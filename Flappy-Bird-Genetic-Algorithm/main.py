import sys
from pygame.sprite import Group
from objects import Background, Pipes, BigText, SmallText
from objects.bird_flock import BirdFlock
from init import *
from config import GAME_FPS, MODE_MENU, MODE_PLAYER, MODE_AI

class App:
    """Quản lý vòng lặp và trạng thái chung của game (Vòng đời game)."""
    def __init__(self):
        """Khởi tạo các đối tượng game (chim, ống, nền, văn bản) và nhóm sprite."""

        # Thiết lập chế độ game ban đầu
        self.game_mode = MODE_MENU

        # Cấu hình nút
        # Tạo font cho nút
        btn_font = pygame.font.SysFont("arial", 60, bold=True)

        # Cấu hình nút START
        self.rect_player = pygame.Rect(0, 0, 260, 80) 
        self.rect_player.center = (GAME_WIDTH // 2, 350)
        self.text_player = btn_font.render("START", True, (255, 255, 255))
        self.text_player_rect = self.text_player.get_rect(center=self.rect_player.center)

        # Cấu hình nút AI
        self.rect_ai = pygame.Rect(0, 0, 260, 80)
        self.rect_ai.center = (GAME_WIDTH // 2, 450)
        self.text_ai = btn_font.render("AI", True, (255, 255, 255))
        self.text_ai_rect = self.text_ai.get_rect(center=self.rect_ai.center)

        self._running = True
        self._display_surf = None

        # Khởi tạo các đối tượng game
        self.bird_flock = BirdFlock()
        self.background = Background()

        # Khởi tạo các đối tượng văn bản
        self.generation_text = None
        self.survival_text = None
        self.max_score_text = None

        # Thời gian sống của người chơi cuối cùng
        self.last_player_time = 0  

        # Lưu mảng các ống cản
        self.pipes = []

        # Thêm các sprite chính
        self.all_sprites = Group()
        self.all_sprites.add(self.background)
        self.all_sprites.add(*self.pipes)
        self.all_sprites.add(*self.bird_flock.get_birds())

        # Thiết lập tiêu đề game
        self.title_font = pygame.font.SysFont("arial", 80, bold=True)
        self.title_shadow = self.title_font.render("FLAPPY BIRD", True, (0, 0, 0))
        self.title_shadow_rect = self.title_shadow.get_rect(center=(GAME_WIDTH // 2 + 5, 105))

        self.title_surf = self.title_font.render("FLAPPY BIRD", True, (255, 255, 255))
        self.title_rect = self.title_surf.get_rect(center=(GAME_WIDTH // 2, 100))

    def on_init(self):
        """Thiết lập màn hình Pygame và cờ chạy game."""
        self._display_surf = DISPLAY_SURFACE
        self._running = True

    def on_event(self, event):
        """Xử lý các sự kiện từ người dùng (như thoát game)."""
        if event.type == QUIT:
            self._running = False

        # Xử lý nhấp chuột vào nút trong menu
        if event.type == MOUSEBUTTONDOWN and self.game_mode == MODE_MENU:
            if self.rect_player.collidepoint(event.pos):
                self.start_player_mode()
            elif self.rect_ai.collidepoint(event.pos):
                self.start_ai_mode()

        # Player nhảy
        if event.type == KEYDOWN:
            if event.key == K_SPACE and self.game_mode == MODE_PLAYER:
                bird = self.bird_flock.get_birds()[0]
                if not bird.dead:
                    bird.flap()

    def on_loop(self):
        """Cập nhật logic game: di chuyển, kiểm tra va chạm, tạo ống, tiến hóa chim."""
        # Xóa các ống và chim không còn hợp lệ
        self.remove_pipes()
        self.remove_birds(self.pipes)

        # Tạo ống mới
        self.generate_pipe()

        # Kiểm tra chim đã chết hết chưa
        if self.bird_flock.is_all_dead(self.pipes):
            # Nếu là chế độ AI, khởi động lại game và tiến hóa chim
            if self.game_mode == MODE_AI:
                self.restart()
            # nếu là chế độ PLAYER thì quay về menu
            else: 
                # Lưu lại thời gian sống của chim player
                self.last_player_time = self.bird_flock.get_birds()[0].score // 60 
                self.game_mode = MODE_MENU

        # Tăng điểm cho các chim còn sống
        self.bird_flock.increase_score()

        # Di chuyển chim
        self.bird_flock.move()

        # Kiểm tra chim có cần ra quyết định không
        if self.game_mode == MODE_AI:
            self.bird_flock.make_decision(self.pipes)

        # Cập nhật văn bản trên màn hình
        self.change_generation_text(self.bird_flock.current_generation)
        self.change_survival_text(self.bird_flock.current_survival_time // 60)
        self.change_max_score_text(self.bird_flock.all_time_max_survival_time // 60)

        # Di chuyển các ống
        for pipe in self.pipes:
            pipe.move()

    def on_render(self):
        """Vẽ tất cả các đối tượng (sprite) lên màn hình."""
        # Vẽ menu
        if self.game_mode == MODE_MENU:
            self._display_surf.blit(self.background.surf, (0, 0)) 

            # Vẽ tiêu đề
            self._display_surf.blit(self.title_shadow, self.title_shadow_rect)
            self._display_surf.blit(self.title_surf, self.title_rect)

            # Vẽ nút START
            pygame.draw.rect(self._display_surf, (46, 204, 113), self.rect_player, border_radius=15)
            pygame.draw.rect(self._display_surf, (255, 255, 255), self.rect_player, 3, border_radius=15) # Vien trang
            self._display_surf.blit(self.text_player, self.text_player_rect)

            # Vẽ nút AI
            pygame.draw.rect(self._display_surf, (230, 126, 34), self.rect_ai, border_radius=15)
            pygame.draw.rect(self._display_surf, (255, 255, 255), self.rect_ai, 3, border_radius=15) # Vien trang
            self._display_surf.blit(self.text_ai, self.text_ai_rect)

            # Nếu đã chơi Player trước đó, hiển thị thời gian sống
            if hasattr(self, 'last_player_time') and self.last_player_time > 0:
                font = pygame.font.SysFont("arial", 50, bold=True)
                score_str = f"Last Player Time: {self.last_player_time} s"
                
                shadow_surf = font.render(score_str, True, (0, 0, 0))
                shadow_rect = shadow_surf.get_rect(center=(GAME_WIDTH // 2 + 3, 203))
                
                text_surf = font.render(score_str, True, (255, 255, 0))
                text_rect = text_surf.get_rect(center=(GAME_WIDTH // 2, 200))

                self._display_surf.blit(shadow_surf, shadow_rect)
                self._display_surf.blit(text_surf, text_rect)
            
            pygame.display.update()
            return

        # Vẽ tất cả sprite trong game
        for sprite in self.all_sprites:
            if isinstance(sprite, Pipes):
                self._display_surf.blit(sprite.first_pipe, sprite.first_rect)
                self._display_surf.blit(sprite.second_pipe, sprite.second_rect)
            else:
                self._display_surf.blit(sprite.surf, sprite.rect)

        # Cập nhật màn hình và giữ FPS
        pygame.display.update()
        FRAME_PER_SEC.tick(GAME_FPS)

    def on_cleanup(self):
        """Dọn dẹp và thoát khỏi Pygame."""
        pygame.quit()
        sys.exit()

    def on_execute(self):
        """Chạy vòng lặp chính của ứng dụng game."""
        if self.on_init() == False:
            self._running = False
        
        # Vòng lặp chính 
        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def remove_pipes(self):
        """Xóa các cặp ống đã ra khỏi màn hình"""
        if len(self.pipes) > 0:
            first_pipe = self.pipes[0]
            if first_pipe.first_rect.right <= 0:
                self.all_sprites.remove(first_pipe)
                self.pipes.pop(0)

    def remove_birds(self, pipes):
        """Xóa (gỡ khỏi sprite group) các chim đã chết."""
        for bird in self.bird_flock.get_birds():
            if bird.is_dead(pipes):
                self.all_sprites.remove(bird)

    def generate_pipe(self):
        """Tạo cặp ống mới nếu số lượng ống hiện tại < 2"""
        if len(self.pipes) < 2:
            new_pipes = Pipes.generate_pipes()
            for new_pipe in new_pipes:
                self.pipes.append(new_pipe)
                self.all_sprites.add(new_pipe)

    def restart(self):
        """Khởi động lại game và tiến hành tiến hóa quần thể chim (thế hệ mới)."""
        self._running = True

        # Nếu ở chế độ AI thì tiến hóa chim
        if self.game_mode == MODE_AI:
            if self.bird_flock.best_bird is not None:
                # Tiến hóa sang thế hệ mới
                self.bird_flock.evolve()
            else:
                # Lần đầu chạy AI, chưa có best_bird
                self.bird_flock.reset_ai_birds() 
                
        # Nếu ở chế độ PLAYER thì đặt lại trạng thái chim người chơi
        elif self.game_mode == MODE_PLAYER:
            # Đặt lại trạng thái chim người chơi
            self.bird_flock.reset_player_bird()
            self.bird_flock.current_survival_time = 0

        # Khởi tạo lại các đối tượng game
        self.background = Background()

        # Lưu mảng ống
        self.pipes = []

        # Xóa tất cả sprite cũ
        self.all_sprites.clear(DISPLAY_SURFACE, self.background.surf)

        # Thêm sprite chính mới
        self.all_sprites = Group()
        self.all_sprites.add(self.background)
        self.all_sprites.add(*self.pipes)
        self.all_sprites.add(*self.bird_flock.get_birds())

    def start_player_mode(self):
        """Bắt đầu chế độ chơi người chơi."""
        self.game_mode = MODE_PLAYER
        self.restart()

    def start_ai_mode(self):
        """Bắt đầu chế độ chơi AI."""
        self.game_mode = MODE_AI
        self.bird_flock = BirdFlock()  
        self.bird_flock.reset_ai_birds()
        self.restart() 

    def change_generation_text(self, generation: int):
        """Cập nhật và hiển thị số thế hệ hiện tại."""
        # Xóa text thế hệ trước
        if self.generation_text:
            self.all_sprites.remove(self.generation_text)

        # Tạo text mới
        self.generation_text = BigText(f"Generation: {generation}")
        self.generation_text.rect.center = (GAME_WIDTH / 2, 50)

        # Vẽ text lên màn hình
        self.all_sprites.add(self.generation_text)

    def change_survival_text(self, survival_time: int):
        """Cập nhật và hiển thị thời gian sống (điểm) hiện tại."""
        # Xóa text thời gian sống trước
        if self.survival_text:
            self.all_sprites.remove(self.survival_text)

        # Tạo text mới
        self.survival_text = SmallText(f"Time: {survival_time} (s)")
        self.survival_text.rect.center = (GAME_WIDTH / 2, 90)

        # Vẽ text lên màn hình
        self.all_sprites.add(self.survival_text)

    def change_max_score_text(self, survival_time: int):
        """Cập nhật và hiển thị kỷ lục thời gian sống tốt nhất."""
        # Xóa text điểm cao trước
        if self.max_score_text:
            self.all_sprites.remove(self.max_score_text)

        # Tạo text mới
        self.max_score_text = SmallText(f"Max: {survival_time} (s)")
        self.max_score_text.rect.center = (GAME_WIDTH / 2, 120)

        # Vẽ text lên màn hình
        self.all_sprites.add(self.max_score_text)

if __name__ == "__main__":
    # Khởi chạy ứng dụng
    app = App()
    app.on_execute()
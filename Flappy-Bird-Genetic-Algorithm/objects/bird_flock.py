from objects.bird import Bird
from ai.genetic_engine import breed_bird, clone_bird


class BirdFlock:
    """Quản lý quần thể chim, bao gồm sinh sản, tiến hóa và cập nhật trạng thái chung."""
    def __init__(self, num_birds=600):
        """
        Khởi tạo quần thể chim với số lượng mặc định.

        :param num_birds: Số lượng chim trong quần thể.
        """

        # Lưu số lượng chim hiện tại
        self.num_birds = num_birds

        # Tạo đàn chim ban đầu
        self.birds = [Bird() for _ in range(num_birds)]

        # Lưu số thế hệ hiện tại
        self.current_generation = 1

        # Lưu thời gian sống (score) hiện tại và kỷ lục mọi thời đại
        self.current_survival_time = 0
        self.all_time_max_survival_time = 0

        # Lưu con chim tốt nhất (best bird) đạt điểm cao nhất từ trước đến nay
        self.best_bird = None

    def get_birds(self):
        """Trả về danh sách các đối tượng chim."""
        return self.birds

    def is_all_dead(self, pipes):
        """
        Kiểm tra xem tất cả các con chim trong đàn đã chết hết chưa.

        :param pipes: Danh sách các ống cản.
        :return: True nếu tất cả chim đã chết, ngược lại False.
        """
        for bird in self.birds:
            bird.is_dead(pipes)
            if not bird.dead:
                return False

        return True

    def move(self):
        """Cập nhật vị trí và vận tốc cho tất cả các chim còn sống."""
        for bird in self.birds:
            if not bird.dead:
                bird.move()

    def make_decision(self, pipes):
        """Yêu cầu các chim còn sống sử dụng mạng nơ-ron để đưa ra quyết định (nhảy/không nhảy)."""
        for bird in self.birds:
            if not bird.dead:
                bird.make_decision(pipes)

    def increase_score(self):
        """
        Tăng điểm/thời gian sống cho chim còn sống và cập nhật kỷ lục thời gian sống của đàn.
        """
        for bird in self.birds:
            if not bird.dead:
                # Tính toán điểm cho chim
                bird.increase_score()

                # Cập nhật thời gian sống hiện tại và kỷ lục mọi thời đại
                self.current_survival_time = max(self.current_survival_time, bird.score)
                self.all_time_max_survival_time = max(self.all_time_max_survival_time, self.current_survival_time)

                # Lưu con chim tốt nhất
                if bird.score >= self.all_time_max_survival_time:
                    self.best_bird = bird
    
    def reset_ai_birds(self):
        """Khởi tạo quần thể chim AI đầu tiên, chưa có best_bird"""
        self.birds = [Bird() for _ in range(self.num_birds)]
        self.best_bird = None

    def reset_player_bird(self):
        """Khởi tạo lại chim của người chơi (1 con)."""
        self.birds = []
        self.birds.append(Bird())

    def evolve(self):
        """
        Tiến hóa quần thể chim sang thế hệ tiếp theo:
        1. Sắp xếp và chọn ra những cá thể tốt nhất.
        2. Lai tạo (breed) và nhân bản (clone) để tạo ra thế hệ mới.

        :return: None
        """
        # Tăng số thế hệ
        self.current_generation += 1

        # Đặt lại thời gian sống cho thế hệ mới
        self.current_survival_time = 0

        # Chọn hai chim có điểm cao nhất để làm cha mẹ
        self.birds.sort(key=lambda bird: bird.score, reverse=True)
        bird_mom, bird_dad = self.birds[:2]

        # Tạo ra thế hệ chim mới bằng cách lai tạo và nhân bản từ chim bố mẹ và chim kỷ lục
        self.birds = (
                        # 1. Lai tạo giữa chim mẹ và chim bố
                        # Mục tiêu: kết hợp gen của 2 cá thể tốt để tạo chim con đa dạng
                        breed_bird(bird_mom, bird_dad, num_children=self.num_birds // 6)

                        # 2. Nhân bản chim mẹ
                        # Mục tiêu: giữ lại toàn bộ đặc điểm của chim mẹ nếu nó đang hoạt động tốt
                      + clone_bird(bird_mom, num_children=self.num_birds // 6)

                        # 3. Nhân bản chim bố
                        # Mục tiêu: bảo toàn gen của chim bố cho thế hệ sau
                      + clone_bird(bird_dad, num_children=self.num_birds // 6)

                        # 4. Nhân bản chim kỷ lục (best_bird)
                        # Mục tiêu: giữ lại cá thể xuất sắc nhất từng đạt điểm cao nhất
                      + clone_bird(self.best_bird, num_children=self.num_birds // 6)

                        # 5. Clone chim mẹ bằng phương thức clone()
                        # Mục tiêu: tạo bản sao y hệt chim mẹ (cách clone thủ công)
                      + [bird_mom.clone() for _ in range(self.num_birds // 6)]

                        # 6. Clone chim kỷ lục bằng phương thức clone()
                        # Mục tiêu: tăng số lượng chim mang gen tối ưu nhất
                      + [self.best_bird.clone() for _ in range(self.num_birds // 6)])
        
        
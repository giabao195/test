from typing import List

from pygame.sprite import Sprite
from pygame.image import load

import numpy as np

from config import (
    GAME_HEIGHT,
    GAME_WIDTH,
    BIRD_ASSET,
    BIRD_ACCEL,
    BIRD_FLAP_STRENGTH
)
from init import Vector2D
from ai import Brain


class Bird(Sprite):
    """Đại diện cho một con chim trong trò chơi, được điều khiển bởi một Mạng Nơ-ron (Brain)."""
    def __init__(self):
        # Khởi tạo hình ảnh (sprite)
        super().__init__()
        self.surf = load(BIRD_ASSET)
        self.rect = self.surf.get_rect(
            center=(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        )

        # Khởi tạo các thông số chuyển động
        self.pos = Vector2D(GAME_WIDTH / 2, GAME_HEIGHT / 2)
        self.velocity = Vector2D(0, 0) # Vận tốc
        self.acceleration = Vector2D(0, BIRD_ACCEL)  # Gia tốc (trọng lực)
        self.flap_strength = Vector2D(0, -BIRD_FLAP_STRENGTH)  # Lực nhảy

        # Tạo bộ não (Brain) của chim
        self.brain = Brain()

        # Cờ kiểm tra trạng thái chết
        self.dead = False

        # Khởi tạo điểm số - thời gian chim đã sống sót (theo frame)
        self.score = 0

    def move(self):
        """Cập nhật vị trí của chim dựa trên vận tốc và gia tốc."""
        # Cập nhật vận tốc (v = v + a)
        self.velocity += self.acceleration
        # Cập nhật vị trí (pos = pos + v)
        self.pos += self.velocity

        # Cập nhật vị trí của rectangle hiển thị
        self.rect.midbottom = self.pos

    def make_decision(self, pipes):
        """
        Thu thập thông tin đầu vào (vision) và chuyển cho bộ não AI để đưa ra quyết định (nhảy/không nhảy).
        :param pipes: Danh sách các ống cản hiện tại.
        """
        # Lấy thông tin đầu vào cho mạng nơ-ron
        vision = self.get_vision(pipes)

        # Truyền qua bộ não và thực hiện hành động nếu mạng nơ-ron trả về True
        if self.brain.perform_action(vision):
            self.flap()

    def flap(self):
        """Thực hiện hành động nhảy (đặt lại vận tốc theo hướng lên)."""
        # Lực nhảy áp dụng thẳng vào vận tốc
        self.velocity = Vector2D(0, -BIRD_FLAP_STRENGTH)

    def increase_score(self):
        """Tăng điểm số (thời gian sống sót) thêm 1 frame."""
        self.score += 1

    def _has_drop_below_screen(self):
        """
        Kiểm tra chim có rơi xuống dưới màn hình (chạm đất) không.
        :return: True nếu chạm đất, ngược lại False.
        """
        return self.rect.bottomleft[1] >= GAME_HEIGHT

    def _has_collided_with_pipes(self, pipes: List):
        """
        Kiểm tra chim có va chạm với bất kỳ cặp ống nào không.
        :param pipes: Danh sách các ống cản.
        :return: True nếu va chạm, ngược lại False.
        """
        for pipe in pipes:
            # Va chạm với ống trên
            if self.rect.colliderect(pipe.first_rect):
                return True
            # Va chạm với ống dưới
            if self.rect.colliderect(pipe.second_rect):
                return True

        return False

    def is_dead(self, pipes: List):
        """
        Kiểm tra trạng thái chết của chim (va chạm với đất hoặc ống cản).
        :return: True nếu chim đã chết, ngược lại False.
        """
        if self._has_drop_below_screen() or self._has_collided_with_pipes(pipes):
            self.dead = True
            return True

    def get_vision(self, pipes):
        """
        Tính toán và trả về vector đầu vào (vision) cho mạng nơ-ron.
        Input vector bao gồm 5 giá trị (theo thứ tự):
        1. bird_y_pos: Tọa độ y của chim.
        2. bird_velocity: Vận tốc y hiện tại của chim.
        3. bird_dist_x: Khoảng cách x đến ống cản tiếp theo.
        4. bird_dist_y_bottom: Khoảng cách y đến miệng ống dưới.
        5. bird_dist_y_top: Khoảng cách y đến miệng ống trên.

        :param pipes: Danh sách các ống cản.
        :return: Vector numpy (5 phần tử) là input cho mạng nơ-ron.
        """
        # Lấy vị trí và vận tốc của chim
        bird_y_pos = self.rect.centery + 0.0
        bird_velocity = self.velocity.y + 0.0

        # Khởi tạo các giá trị khoảng cách
        bird_dist_x = 0
        bird_dist_y_bottom = 0
        bird_dist_y_top = 0

        # Tìm ống cản tiếp theo (ống có x lớn hơn vị trí chim)
        for pipe in pipes:
            # Kiểm tra nếu ống nằm ở bên phải chim
            if pipe.first_rect.midtop[0] >= self.rect.centerx:
                # 3. Khoảng cách X từ chim đến ống
                bird_dist_x = pipe.first_rect.midtop[0] - self.rect.centerx + 0.0
                # 4. Khoảng cách Y (từ tâm chim đến miệng ống dưới)
                bird_dist_y_bottom = self.rect.centery - pipe.first_rect.midtop[1] + 0.0
                # 5. Khoảng cách Y (từ tâm chim đến miệng ống trên)
                bird_dist_y_top = pipe.second_rect.midbottom[1] - self.rect.centery + 0.0
                break # Đã tìm thấy ống gần nhất, thoát vòng lặp

        # Trả về vector đầu vào (vision)
        return np.array(
            [
                bird_y_pos,
                bird_velocity,
                bird_dist_x,
                bird_dist_y_bottom,
                bird_dist_y_top
            ]
        )

    def clone(self):
        """
        Tạo bản sao của chim hiện tại, truyền bộ não (gene) sang bản sao.
        :return: Một con chim mới với cùng cấu trúc não bộ.
        """
        # Tạo một con chim mới
        new_bird = Bird()

        # Truyền gene (các ma trận trọng số W1, b1, W2, b2) sang bộ não chim mới
        new_bird.brain.receive_genes(
            W1=self.brain.W1,
            b1=self.brain.b1,
            W2=self.brain.W2,
            b2=self.brain.b1
        )

        return new_bird
    
    
import random

from pygame.sprite import Sprite
from pygame.image import load

from config import (
    PIPE_SPAWN,
    PIPE_SPAWN_GAP,
    PIPE_VELOCITY,
    PIPE_GAP,
    PIPE_ASSET_1,
    PIPE_ASSET_2
)
from init import Vector2D


class Pipes(Sprite):
    """Đại diện cho một cặp ống cản (ống trên và ống dưới) di chuyển ngang."""
    @staticmethod
    def generate_pipes():
        """
        Phương thức tĩnh. Sinh ra hai cặp ống cản mới với vị trí ngẫu nhiên.
        :return: Danh sách chứa hai đối tượng Pipes.
        """
        # Tạo tọa độ Y ngẫu nhiên cho hai cặp ống
        y_1 = random.randint(300, 600)
        y_2 = random.randint(300, 600)
        # Tạo và trả về hai cặp ống: cặp thứ nhất ở PIPE_SPAWN, cặp thứ hai cách đó một khoảng
        return [Pipes(PIPE_SPAWN, y_1), Pipes(PIPE_SPAWN + PIPE_SPAWN_GAP, y_2)]

    def __init__(self, x, y):
        """
        Khởi tạo cặp ống tại vị trí X cho trước và chiều cao Y (vị trí miệng ống dưới).
        :param x: Tọa độ X ban đầu.
        :param y: Tọa độ Y của miệng ống dưới (topleft của ống dưới).
        """
        # Khởi tạo sprite
        super().__init__()

        # Tạo ống dưới (first pipe)
        self.first_pipe = load(PIPE_ASSET_1)
        self.first_rect = self.first_pipe.get_rect(
            topleft=(x, y)
        )

        # Tạo ống trên (second pipe)
        self.second_pipe = load(PIPE_ASSET_2)
        self.second_rect = self.second_pipe.get_rect(
            bottomleft=(x, y - PIPE_GAP) # Ống trên nằm cách ống dưới một khoảng PIPE_GAP
        )

        # Khởi tạo vị trí và vận tốc (vector) cho ống
        self.first_pos = Vector2D(x, y)
        self.second_pos = Vector2D(x, y - PIPE_GAP)
        self.velocity = Vector2D(-PIPE_VELOCITY, 0) # Vận tốc di chuyển sang trái

    def move(self):
        """
        Di chuyển cặp ống theo vận tốc đã thiết lập.
        :return: None
        """
        # Cập nhật vị trí (pos = pos + v)
        self.first_pos += self.velocity
        self.second_pos += self.velocity
        # Cập nhật rect hiển thị
        self.first_rect.topleft = self.first_pos
        self.second_rect.bottomleft = self.second_pos

        
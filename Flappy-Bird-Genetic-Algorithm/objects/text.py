from pygame.sprite import Sprite
from pygame.font import SysFont


# Khởi tạo font chữ lớn (Big Font)
BIG_FONT = SysFont('timenewsroman', 60)
# Khởi tạo font chữ nhỏ (Small Font)
SMALL_FONT = SysFont('timenewsroman', 40)


class BigText(Sprite):
    """Đại diện cho văn bản lớn (như số thế hệ) hiển thị trên màn hình."""
    def __init__(self, text):
        """
        Khởi tạo văn bản.
        :param text: Nội dung chuỗi cần hiển thị.
        """
        # Khởi tạo sprite
        super().__init__()
        # Render bề mặt văn bản với font lớn, màu trắng
        self.surf = BIG_FONT.render(text, True, (255, 255, 255))
        self.rect = self.surf.get_rect()


class SmallText(Sprite):
    """Đại diện cho văn bản nhỏ (như điểm số/kỷ lục) hiển thị trên màn hình."""
    def __init__(self, text):
        """
        Khởi tạo văn bản.
        :param text: Nội dung chuỗi cần hiển thị.
        """
        # Khởi tạo sprite
        super().__init__()
        # Render bề mặt văn bản với font nhỏ, màu trắng
        self.surf = SMALL_FONT.render(text, True, (255, 255, 255))
        self.rect = self.surf.get_rect()


        
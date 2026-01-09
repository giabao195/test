from pygame.sprite import Sprite
from pygame.image import load


class Background(Sprite):
    """Đại diện cho hình nền tĩnh của trò chơi."""
    def __init__(self):
        """Tải hình nền từ file và thiết lập kích thước (rect)."""
        super().__init__()
        self.surf = load("assets/background/background.png")
        self.rect = self.surf.get_rect()


        
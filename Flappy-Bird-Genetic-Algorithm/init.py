# Nhập thư viện PyGame
import pygame
from pygame.locals import *

# Khởi tạo vector
Vector2D = pygame.math.Vector2

# Khởi tạo Pygame
pygame.init()

# Nhập các biến cấu hình
from config import GAME_HEIGHT, GAME_WIDTH, GAME_TITLE

# Tạo đối tượng đồng hồ (clock)
FRAME_PER_SEC = pygame.time.Clock()

# Tạo bề mặt hiển thị
DISPLAY_SURFACE = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

# Đặt tiêu đề cho cửa sổ hiển thị
pygame.display.set_caption(GAME_TITLE)


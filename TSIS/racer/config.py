import pygame

pygame.init()

# Window
WIDTH, HEIGHT = 500, 700
FPS = 60
ROAD_SCROLL = 6

# Fonts
FONT = pygame.font.SysFont("Arial", 20)
BIG_FONT = pygame.font.SysFont("Arial", 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 120, 255)
ORANGE = (255, 140, 0)
GRAY = (120, 120, 120)
YELLOW = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Powerup colors
SHIELD_COLOR = (0, 120, 255)
NITRO_COLOR = (255, 140, 0)
REPAIR_COLOR = (200, 0, 0)

# Files
LEADERBOARD_FILE = "leaderboard.json"

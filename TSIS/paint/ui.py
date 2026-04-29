import pygame
from config import TOOLBAR_W, WHITE

# Палитра цветов
class Palette:
    def __init__(self, colors):
        self.colors = colors
        self.rects = []

    def draw(self, screen, active_color, top):
        sw = (TOOLBAR_W - 16)//len(self.colors)
        self.rects = []
        for i, col in enumerate(self.colors):
            r = pygame.Rect(8 + i*sw, top, sw-2, 28)
            self.rects.append(r)
            pygame.draw.rect(screen, col, r, border_radius=4)
            if col == active_color:
                pygame.draw.rect(screen, WHITE, r, 2, border_radius=4)

# Простая кнопка
class Button:
    def __init__(self, rect, text, font):
        self.rect, self.text, self.font = rect, text, font

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        txt = self.font.render(self.text, True, WHITE)
        screen.blit(txt, (self.rect.centerx - txt.get_width()//2,
                          self.rect.centery - txt.get_height()//2))

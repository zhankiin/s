import pygame
from config import FONT, GRAY, WHITE


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)
        text_surface = FONT.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

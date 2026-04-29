import pygame
from config import WIDTH, HEIGHT, CELL, LIGHT_GREEN, DARK_GREEN, WHITE

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Bandal", 28)


def draw_text(text, x, y, selected=False):
    color = (255, 255, 0) if selected else WHITE
    screen.blit(font.render(text, True, color), (x, y))


def draw_bg():
    for r in range(HEIGHT // CELL):
        for c in range(WIDTH // CELL):
            color = LIGHT_GREEN if (r + c) % 2 == 0 else DARK_GREEN
            rect = pygame.Rect(c * CELL, r * CELL, CELL, CELL)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 60, 0), rect, 1)
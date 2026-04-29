# pygame.mixer.music - for streaming longer audio tracks (background music)
# Unlike pygame.mixer.Sound (for short effects), music streams from disk
# and only one music track can play at a time

import pygame
import sys
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((600, 400))




running = True
clock = pygame.time.Clock()

player = MusicPlayer()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            if event.key == pygame.K_s:
                player.stop()
            if event.key == pygame.K_n:
                player.next()
            if event.key == pygame.K_b:
                player.prev()
            if event.key == pygame.K_q:
              pygame.quit()
              sys.exit()

    screen.fill("red")
    font = pygame.font.SysFont("Verdana", 20)
    screen.blit(font.render("P = play, S = stop, N = Next, B = previous, Q=quit", True, "green"), (10, 80))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
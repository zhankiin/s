import pygame
from ball import Ball

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

ball = Ball(50, 50, 25, 20)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.KEYDOWN:
        ball.move(event.key, width, height)

    screen.fill((255, 255, 255))
    ball.draw(screen)
    
    clock = pygame.time.Clock()
    clock.tick(60)

    pygame.display.flip()

pygame.quit()
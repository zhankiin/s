import pygame

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    color = (0, 0, 255)
    points = []
    mode = "brush"
    start_pos = None
    radius = 15

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)

                elif event.key == pygame.K_1:
                    mode = 'brush'
                elif event.key == pygame.K_2:
                    mode = 'rectangle'
                elif event.key == pygame.K_3:
                    mode = 'circle'
                elif event.key == pygame.K_4:
                    mode = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    end_pos = event.pos

                    if mode == 'rectangle':
                        rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                        pygame.draw.rect(screen, color, rect, 2)

                    elif mode == 'circle':
                        dx = end_pos[0] - start_pos[0]
                        dy = end_pos[1] - start_pos[1]
                        radius_circle = int((dx**2 + dy**2) ** 0.5)
                        pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if mode == 'brush':
                        points.append(event.pos)
                        points = points[-256:]

                    elif mode == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, 20)

        if mode == 'brush':
            for i in range(len(points) - 1):
                drawLineBetween(screen, points[i], points[i + 1], radius, color)

        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))
    
    for i in range(iterations):
        progress = i / iterations
        x = int(start[0] + (end[0] - start[0]) * progress)
        y = int(start[1] + (end[1] - start[1]) * progress)
        pygame.draw.circle(screen, color, (x, y), width)


main()
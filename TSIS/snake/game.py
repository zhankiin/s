import pygame
import random

from ui import screen, draw_bg, draw_text
from config import WIDTH, HEIGHT, CELL, PADDING, settings


# =========================
# RANDOM POSITION
# =========================

def random_position(snake, obstacles):
    while True:
        pos = (
            random.randint(0, WIDTH // CELL - 1) * CELL,
            random.randint(0, HEIGHT // CELL - 1) * CELL
        )
        if pos not in snake and pos not in obstacles:
            return pos


# =========================
# POWERUPS
# =========================

def spawn_powerup(snake, obstacles):
    if random.random() < 0.01:
        return random.choice(["speed", "slow", "shield"]), random_position(snake, obstacles)
    return None, None


# =========================
# GAME LOOP (FIXED)
# =========================

def game(player_id, best):

    snake = [(100, 100)]
    direction = (CELL, 0)

    obstacles = []

    food = random_position(snake, obstacles)
    food_type = "apple"
    food_val = 1

    poison = None
    poison_timer = 0

    powerup = None
    power_pos = None
    effect = None
    effect_end = 0

    score = 0
    level = 1
    lives = 3

    base_speed = {1: 8, 2: 10, 3: 14}[settings["difficulty"]]
    speed = base_speed

    clock = pygame.time.Clock()  # 🔥 ВАЖНО: возвращаем FPS контроль

    while True:

        draw_bg()

        # =========================
        # EVENTS
        # =========================
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:

                if settings["controls"] == "WASD":
                    if e.key == pygame.K_w and direction != (0, CELL):
                        direction = (0, -CELL)
                    if e.key == pygame.K_s and direction != (0, -CELL):
                        direction = (0, CELL)
                    if e.key == pygame.K_a and direction != (CELL, 0):
                        direction = (-CELL, 0)
                    if e.key == pygame.K_d and direction != (-CELL, 0):
                        direction = (CELL, 0)

                else:
                    if e.key == pygame.K_UP and direction != (0, CELL):
                        direction = (0, -CELL)
                    if e.key == pygame.K_DOWN and direction != (0, -CELL):
                        direction = (0, CELL)
                    if e.key == pygame.K_LEFT and direction != (CELL, 0):
                        direction = (-CELL, 0)
                    if e.key == pygame.K_RIGHT and direction != (-CELL, 0):
                        direction = (CELL, 0)

        # =========================
        # MOVE SNAKE
        # =========================
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # WALL COLLISION
        if not (0 <= head[0] < WIDTH and 0 <= head[1] < HEIGHT):
            if effect != "shield":
                break

        # SELF COLLISION
        if head in snake:
            if effect != "shield":
                break

        # OBSTACLE COLLISION
        if head in obstacles:
            if effect != "shield":
                break

        snake.insert(0, head)

        # =========================
        # FOOD
        # =========================
        if head == food:
            score += food_val
            food = random_position(snake, obstacles)

            food_type = random.choice(["apple", "pear", "peach"])
            food_val = {"apple": 1, "pear": 2, "peach": 3}[food_type]

            # LEVEL SYSTEM (ВОЗВРАЩЕН КАК БЫЛО)
            if score % 5 == 0:
                level += 1
                speed += 2
                obstacles.append(random_position(snake, obstacles))

        else:
            snake.pop()

        # =========================
        # POWERUPS
        # =========================
        if powerup is None:
            powerup, power_pos = spawn_powerup(snake, obstacles)

        if powerup and head == power_pos:
            if powerup == "speed":
                speed += 5
                effect = "speed"
                effect_end = pygame.time.get_ticks() + 5000

            elif powerup == "slow":
                speed = max(5, speed - 5)
                effect = "slow"
                effect_end = pygame.time.get_ticks() + 5000

            elif powerup == "shield":
                effect = "shield"
                effect_end = pygame.time.get_ticks() + 5000

            powerup = None

        # EFFECT END
        if effect and pygame.time.get_ticks() > effect_end:
            speed = base_speed + (level - 1) * 2
            effect = None

        # =========================
        # DRAW
        # =========================

        for s in snake:
            pygame.draw.rect(screen, (180, 0, 0),
                             (s[0] + PADDING // 2, s[1] + PADDING // 2, CELL - PADDING, CELL - PADDING))

        pygame.draw.rect(screen, (0, 255, 0),
                         (food[0] + PADDING // 2, food[1] + PADDING // 2, CELL - PADDING, CELL - PADDING))

        draw_text(f"Score:{score}", 10, 10)
        draw_text(f"Level:{level}", 10, 40)
        draw_text(f"Best:{best}", 10, 70)
        draw_text(f"Lives:{lives}", 10, 100)

        pygame.display.flip()
        clock.tick(speed)

    return score, level
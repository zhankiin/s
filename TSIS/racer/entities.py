import pygame
import random
from config import (
    WIDTH, HEIGHT, ROAD_SCROLL,
    YELLOW, SILVER, BRONZE, BLACK, GRAY, ORANGE,
    SHIELD_COLOR, NITRO_COLOR, REPAIR_COLOR
)
from assets import PLAYER_IMG, ENEMY_IMG


# =========================
# Игрок
# =========================
class Player:
    def __init__(self):
        self.reset()  # начальные параметры
        self.speed = 6  # скорость движения

    def reset(self):
        # стартовая позиция игрока
        self.x = WIDTH // 2
        self.y = HEIGHT - 120

        # здоровье и усиления
        self.hp = 3
        self.shield = 0
        self.nitro = 0

    def move(self, dx, dy):
        # движение игрока
        self.x += dx * self.speed
        self.y += dy * self.speed

        # ограничение по экрану
        self.x = max(0, min(WIDTH - 50, self.x))
        self.y = max(0, min(HEIGHT - 100, self.y))

    def update(self):
        # уменьшение времени действия бонусов
        if self.shield > 0:
            self.shield -= 1
        if self.nitro > 0:
            self.nitro -= 1

    def draw(self, surface):
        # отрисовка игрока
        surface.blit(PLAYER_IMG, (self.x, self.y))

        # визуальный эффект щита
        if self.shield > 0:
            pygame.draw.circle(
                surface, SHIELD_COLOR,
                (self.x + 25, self.y + 40), 50, 2
            )


# =========================
# Монеты
# =========================
class Coin:
    # типы монет с характеристиками
    TYPES = {
        "bronze": {"value": 1, "color": BRONZE, "radius": 10, "weight": 60},
        "silver": {"value": 3, "color": SILVER, "radius": 8, "weight": 30},
        "gold": {"value": 5, "color": YELLOW, "radius": 6, "weight": 10},
    }

    def __init__(self):
        # случайная позиция сверху экрана
        self.x = random.randint(50, WIDTH - 50)
        self.y = -20

        # выбор типа монеты с вероятностью (weight)
        types = list(self.TYPES.keys())
        weights = [self.TYPES[t]["weight"] for t in types]
        self.type = random.choices(types, weights)[0]

        # параметры выбранной монеты
        info = self.TYPES[self.type]
        self.value = info["value"]
        self.color = info["color"]
        self.radius = info["radius"]

    def update(self):
        # движение вниз по дороге
        self.y += ROAD_SCROLL

    def draw(self, surface):
        # отрисовка монеты
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)


# =========================
# Враги
# =========================
class Enemy:
    def __init__(self, speed):
        self.x = random.randint(50, WIDTH - 100)
        self.y = -100
        self.speed = speed  # индивидуальная скорость врага

    def update(self):
        # движение вниз
        self.y += self.speed

    def draw(self, surface):
        # отрисовка врага
        surface.blit(ENEMY_IMG, (self.x, self.y))


# =========================
# Препятствия на дороге
# =========================
class Obstacle:
    def __init__(self, obstacle_type):
        self.x = random.randint(50, WIDTH - 100)
        self.y = -50
        self.type = obstacle_type  # тип препятствия

    def update(self):
        # движение вниз
        self.y += ROAD_SCROLL

    def draw(self, surface):
        # разные типы препятствий
        if self.type == "barrier":
            pygame.draw.rect(surface, BLACK, (self.x, self.y, 50, 50))
        elif self.type == "speed_bump":
            pygame.draw.rect(surface, GRAY, (self.x, self.y, 50, 20))
        elif self.type == "boost":
            pygame.draw.rect(surface, ORANGE, (self.x, self.y, 50, 20))


# =========================
# Усиления (power-ups)
# =========================
class PowerUp:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -40

        # случайный тип бонуса
        self.type = random.choice(["shield", "nitro", "repair"])

    def update(self):
        # движение вниз
        self.y += ROAD_SCROLL

    def draw(self, surface):
        # цвета бонусов
        colors = {
            "shield": SHIELD_COLOR,
            "nitro": NITRO_COLOR,
            "repair": REPAIR_COLOR
        }

        # отрисовка бонуса
        pygame.draw.circle(surface, colors[self.type], (self.x, int(self.y)), 12)
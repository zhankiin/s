import pygame
import random
import os

# Инициализация pygame
pygame.init()

# Определяем базовую папку проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Формируем пути к ресурсам
car_path = os.path.join(BASE_DIR, "resources", "player.png")
road_path = os.path.join(BASE_DIR, "resources", "road.png")
coin_path = os.path.join(BASE_DIR, "resources", "coin.png")

# Загружаем изображения
car_img = pygame.image.load(car_path)
road_img = pygame.image.load(road_path)
coin_img = pygame.image.load(coin_path)

# Размер окна
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонщик")



# Масштабирование (если нужно)
car_img = pygame.transform.scale(car_img, (50, 120))
coin_img = pygame.transform.scale(coin_img, (50, 50))
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Позиция машины
car_x = WIDTH // 2 - 25
car_y = HEIGHT - 120
car_speed = 5

# Монеты
coins = []
coin_speed = 5

# Счёт
score = 0
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(road_img, (0, 0))  # рисуем дорогу

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление машиной
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < WIDTH - 50:
        car_x += car_speed

    # Случайное появление монет
    if random.randint(1, 50) == 1:
        coin_x = random.randint(0, WIDTH - 30)
        coin_y = -30
        coins.append([coin_x, coin_y])

    # Движение монет
    for coin in coins:
        coin[1] += coin_speed

    # Проверка столкновений
    car_rect = pygame.Rect(car_x, car_y, 50, 100)

    new_coins = []
    for coin in coins:
        coin_rect = pygame.Rect(coin[0], coin[1], 30, 30)

        # Если столкновение — увеличиваем счёт
        if car_rect.colliderect(coin_rect):
            score += 1
        else:
            new_coins.append(coin)

    coins = new_coins

    # Рисуем монеты
    for coin in coins:
        screen.blit(coin_img, (coin[0], coin[1]))

    # Рисуем машину
    screen.blit(car_img, (car_x, car_y))

    # Отображение счёта (правый верхний угол)
    text = font.render(f"Coins: {score}", True, (0, 0, 0))
    screen.blit(text, (WIDTH - 150, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
import pygame
import datetime
import os
import sys

pygame.init()

screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
done = False

# функция безопасной загрузки изображений
def get_image(path):
    if not os.path.exists(path):
        print(f"❌ Ошибка: файл не найден -> {path}")
        print("Файлы в текущей папке:", os.listdir())
        folder = os.path.dirname(path)
        if os.path.exists(folder):
            print(f"Файлы в папке '{folder}':", os.listdir(folder))
        sys.exit(1)  # остановка программы
    return pygame.image.load(path).convert_alpha()

# проверяй путь к файлам
clock_img = get_image('mickeys_clock/images/mickeyclock.jpeg')
minute_hand = get_image('mickeys_clock/images/minute.jpeg')
hour_hand = get_image('mickeys_clock/images/secund.jpeg')

# фон (Микки) масштабируем под окно 400x300
clock_img = pygame.transform.scale(get_image('mickeys_clock/images/mickeyclock.jpeg'), (400, 300))

# стрелки (подбираешь размер под фон)
minute_hand = pygame.transform.scale(get_image('mickeys_clock/images/minute.jpeg'), (60, 60))
hour_hand = pygame.transform.scale(get_image('mickeys_clock/images/secund.jpeg'), (50, 50))

# центр часов (подбери под свою картинку)
pivot = (200, 150)

# вращение стрелок
rotated_minute = pygame.transform.rotate(minute_hand, minute_angle)
rotated_hour = pygame.transform.rotate(hour_hand, hour_angle)

# центрирование вращения вокруг pivot
rect_min = rotated_minute.get_rect(center=pivot)
rect_hour = rotated_hour.get_rect(center=pivot)


screen.blit(clock_img, (0, 0))        # фон Микки
screen.blit(rotated_hour, rect_hour)  # часовая рука
screen.blit(rotated_minute, rect_min) # минутная рука

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # текущее время
    now = datetime.datetime.now()
    minute = now.minute
    hour = now.hour % 12
    second = now.second

    # углы
    minute_angle = -6 * minute - 0.1 * second  # плавное движение минутной стрелки
    hour_angle = -30 * hour - 0.5 * minute
    second_angle = -6 * second

    # вращение стрелок
    rotated_minute = pygame.transform.rotate(minute_hand, minute_angle)
    rotated_hour = pygame.transform.rotate(hour_hand, hour_angle)

    # очистка экрана
    screen.fill((255, 255, 255))

    # рисуем фон
    screen.blit(clock_img, (0, 0))

    # центрирование стрелок
    rect_min = rotated_minute.get_rect(center=center)
    rect_hour = rotated_hour.get_rect(center=center)

    # рисуем стрелки
    screen.blit(rotated_hour, rect_hour)
    screen.blit(rotated_minute, rect_min)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
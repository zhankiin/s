import pygame
import random
from config import (
    WIDTH, HEIGHT, FPS, FONT, BIG_FONT,
    WHITE, BLACK, RED, ORANGE, SHIELD_COLOR
)
from assets import ROAD, play_sound, play_background, stop_background
from entities import Player, Coin, Enemy, Obstacle, PowerUp
from ui import Button
from utils import load_leaderboard, add_score


# =========================
# Основной класс игры
# =========================
class Game:
    def __init__(self):
        # Инициализация окна и базовых систем pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Racing Game")

        # Состояние игры (меню / игра / геймовер / таблица)
        self.state = "menu"

        # Игрок
        self.player = Player()

        # Флаг фоновой музыки
        self.background_playing = False

        # Кнопки UI
        self._init_buttons()

        # Сброс состояния игры
        self.reset_game()

    # =========================
    # UI кнопки
    # =========================
    def _init_buttons(self):
        self.buttons = {
            "play": Button(180, 200, 120, 40, "PLAY"),
            "lb": Button(180, 260, 120, 40, "LEADERBOARD"),
            "quit": Button(180, 320, 120, 40, "QUIT"),
            "retry": Button(180, 400, 120, 40, "RESTART"),
            "back": Button(180, 460, 120, 40, "MENU"),
        }

    # =========================
    # Сброс игры
    # =========================
    def reset_game(self):
        self.coins = []
        self.enemies = []
        self.obstacles = []
        self.powerups = []

        self.score = 0
        self.distance = 0

        self.enemy_speed = 4

        # Останавливаем музыку при рестарте
        self._stop_background()

    # =========================
    # Фон
    # =========================
    def _start_background(self):
        if not self.background_playing and self.state == "play":
            play_background()
            self.background_playing = True

    def _stop_background(self):
        if self.background_playing:
            stop_background()
            self.background_playing = False

    # =========================
    # Безопасный спавн объектов (не рядом с игроком)
    # =========================
    def _safe_spawn_x(self):
        for _ in range(10):
            x = random.randint(50, WIDTH - 100)
            if abs(x - self.player.x) > 100:
                return x
        return random.randint(50, WIDTH - 100)

    # =========================
    # Спавн объектов
    # =========================
    def _spawn_entities(self):
        # монеты
        if random.random() < 0.5:
            self.coins.append(Coin())

        # враги
        if random.random() < 0.3:
            enemy = Enemy(self.enemy_speed)
            enemy.x = self._safe_spawn_x()
            self.enemies.append(enemy)

        # препятствия
        if random.random() < 0.3:
            obs = Obstacle(random.choice(["barrier", "speed_bump", "boost"]))
            obs.x = self._safe_spawn_x()
            self.obstacles.append(obs)

        # бонусы
        if random.random() < 0.25:
            powerup = PowerUp()
            powerup.x = self._safe_spawn_x()
            self.powerups.append(powerup)

    # =========================
    # Проверка столкновений
    # =========================
    def _check_collision(self, a, b):
        return abs(a.x - b.x) < 40 and abs(a.y - b.y) < 60

    # =========================
    # Обработка столкновений
    # =========================
    def _handle_collisions(self):

        # -------- Монеты --------
        for coin in self.coins[:]:
            if self._check_collision(coin, self.player):
                self.score += coin.value * 10
                self.coins.remove(coin)
                play_sound("coin")

        # -------- Враги --------
        for enemy in self.enemies[:]:
            if self._check_collision(enemy, self.player):
                if self.player.shield <= 0:
                    self.player.hp -= 1
                    play_sound("hurt")
                else:
                    play_sound("powerup")

                self.enemies.remove(enemy)
                play_sound("crash")

        # -------- Препятствия --------
        for obs in self.obstacles[:]:
            if self._check_collision(obs, self.player):

                if obs.type == "boost":
                    self.enemy_speed += 1
                    play_sound("boost")

                elif obs.type == "barrier" and self.player.shield <= 0:
                    self.player.hp -= 1
                    play_sound("hurt")
                    play_sound("crash")

                self.obstacles.remove(obs)

        # -------- PowerUps --------
        for powerup in self.powerups[:]:
            if self._check_collision(powerup, self.player):

                if powerup.type == "shield":
                    self.player.shield = 300

                elif powerup.type == "nitro":
                    self.player.nitro = 200
                    self.enemy_speed += 1

                elif powerup.type == "repair":
                    self.player.hp = min(3, self.player.hp + 1)

                play_sound("powerup")
                self.powerups.remove(powerup)

        # -------- Game Over --------
        if self.player.hp <= 0 and self.state != "gameover":
            add_score(self.score, self.distance)
            self.state = "gameover"
            play_sound("gameover")
            self._stop_background()

    # =========================
    # Обновление игры
    # =========================
    def _update(self):
        self.distance += 1
        self.score += 1

        self.player.update()

        # обновление всех объектов
        for entity_list in [self.coins, self.enemies, self.obstacles, self.powerups]:
            for entity in entity_list:
                entity.update()

        # удаление вышедших за экран объектов
        self.coins = [c for c in self.coins if c.y < HEIGHT]
        self.enemies = [e for e in self.enemies if e.y < HEIGHT]
        self.obstacles = [o for o in self.obstacles if o.y < HEIGHT]
        self.powerups = [p for p in self.powerups if p.y < HEIGHT]

        self._handle_collisions()

        # случайный спавн
        if random.random() < 0.05:
            self._spawn_entities()

        # запуск музыки
        if not self.background_playing and self.player.hp > 0:
            self._start_background()

    # =========================
    # Рендер игры
    # =========================
    def _draw_game(self):
        self.screen.blit(ROAD, (0, 0))
        self.player.draw(self.screen)

        for entity_list in [self.coins, self.enemies, self.obstacles, self.powerups]:
            for entity in entity_list:
                entity.draw(self.screen)

        # HUD (информация)
        hud_text = f"Score:{self.score} HP:{self.player.hp}"
        self.screen.blit(FONT.render(hud_text, True, WHITE), (10, 10))

        # нитро-бар
        if self.player.nitro > 0:
            nitro_width = int((self.player.nitro / 200) * 100)
            pygame.draw.rect(self.screen, ORANGE, (10, 40, nitro_width, 10))

        # щит
        if self.player.shield > 0:
            shield_text = FONT.render(
                f"SHIELD: {self.player.shield // 60}",
                True,
                SHIELD_COLOR
            )
            self.screen.blit(shield_text, (WIDTH - 100, 10))

    # =========================
    # Меню
    # =========================
    def _draw_menu(self):
        self.screen.fill(BLACK)
        self.screen.blit(BIG_FONT.render("RACER", True, WHITE), (180, 100))

        for name in ["play", "lb", "quit"]:
            self.buttons[name].draw(self.screen)

    # =========================
    # Game Over экран
    # =========================
    def _draw_gameover(self):
        self.screen.fill(BLACK)
        self.screen.blit(BIG_FONT.render("GAME OVER", True, RED), (140, 200))
        self.screen.blit(FONT.render(f"Score:{self.score}", True, WHITE), (180, 280))

        self.buttons["retry"].draw(self.screen)
        self.buttons["back"].draw(self.screen)

    # =========================
    # Таблица рекордов
    # =========================
    def _draw_leaderboard(self):
        self.screen.fill(BLACK)
        self.screen.blit(BIG_FONT.render("LEADERBOARD", True, WHITE), (120, 30))

        data = load_leaderboard()
        y = 120

        if not data:
            self.screen.blit(FONT.render("No scores yet!", True, WHITE), (150, y))
        else:
            for i, entry in enumerate(data):
                text = f"{i + 1}. Score:{entry['score']} Dist:{entry['dist']}"
                self.screen.blit(FONT.render(text, True, WHITE), (120, y))
                y += 30

        self.buttons["back"].draw(self.screen)

    # =========================
    # Обработка кликов меню
    # =========================
    def _handle_menu_click(self, pos):
        if self.buttons["play"].is_clicked(pos):
            self.state = "play"
            self.player.reset()
            self.reset_game()

        elif self.buttons["lb"].is_clicked(pos):
            self.state = "leaderboard"

        elif self.buttons["quit"].is_clicked(pos):
            return False

        return True

    # =========================
    # GameOver клики
    # =========================
    def _handle_gameover_click(self, pos):
        if self.buttons["retry"].is_clicked(pos):
            self.player.reset()
            self.reset_game()
            self.state = "play"

        elif self.buttons["back"].is_clicked(pos):
            self.state = "menu"
            self._stop_background()

    # =========================
    # Главный цикл игры
    # =========================
    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)

            # события
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if self.state == "menu":
                        running = self._handle_menu_click(pos)

                    elif self.state == "gameover":
                        self._handle_gameover_click(pos)

                    elif self.state == "leaderboard":
                        if self.buttons["back"].is_clicked(pos):
                            self.state = "menu"

            # управление игроком
            keys = pygame.key.get_pressed()
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
            dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
            self.player.move(dx, dy)

            # логика + рендер по состояниям
            if self.state == "menu":
                self._draw_menu()

            elif self.state == "play":
                self._update()
                self._draw_game()

            elif self.state == "leaderboard":
                self._draw_leaderboard()

            elif self.state == "gameover":
                self._draw_gameover()

            pygame.display.flip()

        # выход
        self._stop_background()
        pygame.quit()
import pygame
from ui import screen, draw_text
from config import settings


# =========================
# USERNAME INPUT
# =========================

def get_username():
    name = ""
    while True:
        screen.fill((0, 0, 0))
        draw_text("Enter Username:", 280, 250)
        draw_text(name, 280, 300)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name:
                    return name
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += e.unicode

        pygame.display.flip()


# =========================
# MAIN MENU
# =========================

def main_menu():
    options = ["Play", "Leaderboard", "Settings", "Exit"]
    selected = 0

    while True:
        screen.fill((0, 0, 0))

        for i, opt in enumerate(options):
            draw_text(opt, 350, 200 + i * 50, i == selected)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)

                if e.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)

                if e.key == pygame.K_RETURN:
                    return options[selected]

        pygame.display.flip()


# =========================
# SETTINGS MENU
# =========================

def settings_menu():
    sel = 0

    while True:
        screen.fill((0, 0, 0))

        draw_text(f"Difficulty: {settings['difficulty']}", 300, 200, sel == 0)
        draw_text(f"Controls: {settings['controls']}", 300, 250, sel == 1)
        draw_text(f"Grid: {settings['grid']}", 300, 300, sel == 2)
        draw_text("Back", 300, 350, sel == 3)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    sel = (sel - 1) % 4

                if e.key == pygame.K_DOWN:
                    sel = (sel + 1) % 4

                if e.key == pygame.K_RETURN:

                    if sel == 0:
                        settings["difficulty"] = settings["difficulty"] % 3 + 1

                    elif sel == 1:
                        settings["controls"] = "ARROWS" if settings["controls"] == "WASD" else "WASD"

                    elif sel == 2:
                        settings["grid"] = not settings["grid"]

                    elif sel == 3:
                        return

        pygame.display.flip()
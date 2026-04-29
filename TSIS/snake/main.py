import pygame

from menu import get_username, main_menu, settings_menu
from services import get_or_create_player, get_best, save_game
from game import game
from ui import screen


username = get_username()
player_id = get_or_create_player(username)

while True:
    best = get_best(player_id)
    choice = main_menu()

    if choice == "Play":
        score, level = game(player_id, best)
        save_game(player_id, score, level)

    elif choice == "Leaderboard":
        from ui import draw_text
        from services import get_top10

        data = get_top10()
        running = True

        while running:
            screen.fill((0, 0, 0))
            draw_text("TOP 10", 350, 50)

            for i, row in enumerate(data):
                draw_text(f"{i+1}. {row[0]} - {row[1]}", 280, 120 + i * 30)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.KEYDOWN:
                    running = False

            pygame.display.flip()

    elif choice == "Settings":
        settings_menu()

    elif choice == "Exit":
        break

pygame.quit()
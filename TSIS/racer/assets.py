import pygame
import os
from config import WIDTH, HEIGHT

# Images
ROAD = pygame.transform.scale(
    pygame.image.load("AnimatedStreet.png"), 
    (WIDTH, HEIGHT)
)
PLAYER_IMG = pygame.transform.scale(
    pygame.image.load("Player.png"), 
    (50, 90)
)
ENEMY_IMG = pygame.transform.scale(
    pygame.image.load("Enemy.png"), 
    (50, 90)
)


def load_sound(filename):
    """Safely load a sound file."""
    if os.path.exists(filename):
        try:
            return pygame.mixer.Sound(filename)
        except:
            return None
    return None


# Sounds
pygame.mixer.init()

SOUNDS = {
    "background": load_sound("background.wav"),
    "crash": load_sound("crash.wav"),
    "coin": load_sound("coin.wav"),
    "powerup": load_sound("powerup.wav"),
    "hurt": load_sound("hurt.wav"),
    "boost": load_sound("boost.wav"),
    "gameover": load_sound("gameover.wav"),
}


def play_sound(name):
    """Play a sound by name if it exists."""
    sound = SOUNDS.get(name)
    if sound:
        sound.play()


def play_background():
    """Start looping background music."""
    sound = SOUNDS.get("background")
    if sound:
        sound.play(-1)


def stop_background():
    """Stop background music."""
    sound = SOUNDS.get("background")
    if sound:
        sound.stop()

import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()

        base_dir = os.path.dirname(__file__)
        music_dir = os.path.join(base_dir, "music")

        self.playlist = [
            os.path.join(music_dir, "bonk.mp3"),
            os.path.join(music_dir, "kap.mp3"),

        ]

        self.current = 0

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    def prev(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()

    def get_current_track(self):
        return os.path.basename(self.playlist[self.current])

    def get_position(self):
        return pygame.mixer.music.get_pos() // 1000
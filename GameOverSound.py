import pygame
import os
import sys

pygame.init()

def play_game_over():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    GameOverSound = os.path.join(BASE_DIR, "assets", "Music", "GameOver.wav")
    try:
        game_over_track = pygame.mixer.Sound(GameOverSound)
        game_over_track.play()
        track_duration = int(game_over_track.get_length() * 1000)
        pygame.time.wait(track_duration)
    except pygame.error as e:
        print(f"Audio Error: {e}")
        sys.exit()

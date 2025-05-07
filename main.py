# File: main.py
# Entry point for Arcade Survival

import pygame
import sys

# Step 1: Initialize screen first before importing anything that uses it
from config.settings import init_display
init_display()

# Step 2: Now import modules that rely on screen being initialized
from config.settings import clock, FPS, set_volumes
from config.paths import MUSIC_PATH, load_sounds
from core.game import Game

def main():
    # Initialize all pygame modules
    pygame.init()
    pygame.mixer.init()

    # Load all sound effects (must be after mixer.init())
    try:
        load_sounds()
    except Exception as e:
        print(f"[ERROR] Failed to load sound effects: {e}")

    # Load and play background music
    try:
        pygame.mixer.music.load(MUSIC_PATH)
        set_volumes()
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except Exception as e:
        print(f"[ERROR] Failed to load or play music: {e}")

    # Start the game loop
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"[ERROR] Game crashed with error: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()

# File: config/paths.py
# Paths and sound loading logic for music and sound effects

import os
import pygame

# --- Define base directories ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds")

# --- File paths ---
MUSIC_PATH = os.path.join(SOUNDS_DIR, "music.mp3")
SHOOT_PATH = os.path.join(SOUNDS_DIR, "shoot.mp3")
KILL_PATH = os.path.join(SOUNDS_DIR, "kill.mp3")
GAMEOVER_PATH = os.path.join(SOUNDS_DIR, "gameover.mp3")

# --- Internal sound registry ---
_sounds = {}

def load_sounds():
    """
    Loads all sound effects. Must be called after pygame.mixer.init().
    """
    try:
        _sounds["shoot"] = pygame.mixer.Sound(SHOOT_PATH)
        _sounds["kill"] = pygame.mixer.Sound(KILL_PATH)
        _sounds["gameover"] = pygame.mixer.Sound(GAMEOVER_PATH)
    except Exception as e:
        print(f"[ERROR] Failed to load sound: {e}")

def get_sound(name):
    """
    Safely retrieve a sound by name (e.g. 'shoot', 'kill', 'gameover').
    Returns None if sound was not loaded.
    """
    return _sounds.get(name)

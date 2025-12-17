# File: config/paths.py
# Paths and sound/image loading logic

import os
import pygame

# --- Define base directories ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

# --- Sound File paths ---
MUSIC_PATH = os.path.join(SOUNDS_DIR, "music.mp3")
SHOOT_PATH = os.path.join(SOUNDS_DIR, "shoot.mp3")
KILL_PATH = os.path.join(SOUNDS_DIR, "kill.mp3")
GAMEOVER_PATH = os.path.join(SOUNDS_DIR, "gameover.mp3")

# --- Image File paths ---
PLAYER_IMG_PATH = os.path.join(IMAGES_DIR, "player.png")
ENEMY_IMG_PATH = os.path.join(IMAGES_DIR, "enemy.png")
PLAYER_SHEET_PATH = os.path.join(IMAGES_DIR, "player_sheet.png")
ENEMY_SHEET_PATH = os.path.join(IMAGES_DIR, "enemy_sheet.png")
FAST_ENEMY_SHEET_PATH = os.path.join(IMAGES_DIR, "fast_enemy_sheet.png")
TANK_ENEMY_SHEET_PATH = os.path.join(IMAGES_DIR, "tank_enemy_sheet.png")
SHOOTER_ENEMY_SHEET_PATH = os.path.join(IMAGES_DIR, "shooter_enemy_sheet.png")
ENEMY_BULLET_IMG_PATH = os.path.join(IMAGES_DIR, "enemy_bullet.png")
POWERUP_HEALTH_PATH = os.path.join(IMAGES_DIR, "powerup_health.png")
POWERUP_SPEED_PATH = os.path.join(IMAGES_DIR, "powerup_speed.png")
POWERUP_RAPIDFIRE_PATH = os.path.join(IMAGES_DIR, "powerup_rapidfire.png")
BACKGROUND_IMG_PATH = os.path.join(IMAGES_DIR, "background.jpg")

# --- Internal registries ---
_sounds = {}
_images = {}

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

def load_images():
    """
    Loads all game images. Must be called after pygame.display.set_mode() usually, 
    but for simple loading pygame.init() is enough.
    """
    try:
        # Load and convert_alpha for transparency support
        player_img = pygame.image.load(PLAYER_IMG_PATH).convert_alpha()
        enemy_img = pygame.image.load(ENEMY_IMG_PATH).convert_alpha()
        bg_img = pygame.image.load(BACKGROUND_IMG_PATH).convert()

        _images["player"] = player_img
        _images["enemy"] = enemy_img
        _images["background"] = bg_img
    except Exception as e:
        print(f"[ERROR] Failed to load image: {e}")

def get_image(name):
    """
    Safely retrieve an image by name.
    """
    return _images.get(name)

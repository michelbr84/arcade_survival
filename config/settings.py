# File: config/settings.py
# Game-wide configuration settings such as screen resolution, volume, colors, and font

import pygame

# --- Volume Settings ---
master_volume = 1.0
music_volume = 0.5
effects_volume = 1.0

def set_volumes():
    """Set global master volume for music and sound effects."""
    try:
        pygame.mixer.music.set_volume(master_volume)
        from config.paths import get_sound
        for sound_name in ["shoot", "kill", "gameover"]:
            sound = get_sound(sound_name)
            if sound:
                sound.set_volume(master_volume)
    except Exception as e:
        print(f"[ERROR] Failed to set volume: {e}")

# --- Screen Settings ---
RESOLUTIONS = [(800, 600), (1024, 768), (1280, 720), (1600, 900), (1920, 1080)]
current_res_index = 0
fullscreen = False
WIDTH, HEIGHT = RESOLUTIONS[current_res_index]

screen = None  # Will be initialized by init_display()

def init_display():
    global screen, WIDTH, HEIGHT
    WIDTH, HEIGHT = RESOLUTIONS[current_res_index]
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    pygame.display.set_caption("Arcade Survival")

# --- Timing ---
clock = pygame.time.Clock()
FPS = 60

# --- Colors ---
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
YELLOW  = (255, 255, 0)
BLUE    = (0, 128, 255)
GRAY    = (100, 100, 100)

# --- Fonts ---
pygame.font.init()
font = pygame.font.SysFont("arial", 24)

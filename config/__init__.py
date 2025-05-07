# config/__init__.py
# Marks the config directory as a Python package.
# You can optionally preload settings or expose shortcuts here.

from .settings import (
    master_volume,
    music_volume,
    effects_volume,
    set_volumes,
    init_display,
    WIDTH,
    HEIGHT,
    screen,
    clock,
    FPS,
    RESOLUTIONS,
    current_res_index,
    fullscreen,
    WHITE,
    BLACK,
    GREEN,
    RED,
    YELLOW,
    BLUE,
    GRAY,
    font
)

from .paths import MUSIC_PATH, load_sounds, get_sound


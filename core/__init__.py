# core/__init__.py
# Marks the core directory as a Python package.
# Re-exports key components of the game engine.

from .game import Game
from .menus import show_main_menu, show_pause_menu, show_options_menu
from .utils import draw_text, button, resolve_overlap

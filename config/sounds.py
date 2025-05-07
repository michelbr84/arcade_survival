import os
import pygame

class SoundManager:
    _sounds = {}

    def __init__(self):
        self.load_sounds()

    def load_sounds(self):
        """Load all sound effects. Must be called after pygame.mixer.init()."""
        try:
            SHOOT = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "shoot.mp3"))
            KILL = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "kill.mp3"))
            GAMEOVER = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "gameover.mp3"))
        except Exception as e:
            print(f"[ERROR] Failed to load sound: {e}")

    def get_sfx_shoot(self, name="shoot"):
        """Safely retrieve a sound by name (e.g. 'shoot', 'kill', 'gameover')."""
        return self._sounds.get(name)
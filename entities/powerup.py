import pygame
import math
from config.settings import screen, WIDTH, HEIGHT
from config.paths import POWERUP_HEALTH_PATH, POWERUP_SPEED_PATH, POWERUP_RAPIDFIRE_PATH

class PowerUp:
    def __init__(self, x, y, p_type):
        self.x = x
        self.y = y
        self.type = p_type # "health", "speed", "rapid_fire"
        self.radius = 12
        self.life_time = 600 # 10 seconds to pick up before disappearing
        
        path = None
        if self.type == "health": path = POWERUP_HEALTH_PATH
        elif self.type == "speed": path = POWERUP_SPEED_PATH
        elif self.type == "rapid_fire": path = POWERUP_RAPIDFIRE_PATH
        
        try:
            self.image = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (32, 32))
        except Exception:
            self.image = None

    def update(self):
        self.life_time -= 1

    def draw(self):
        if self.image:
             rect = self.image.get_rect(center=(int(self.x), int(self.y)))
             screen.blit(self.image, rect)
        else:
             color = (0, 255, 0)
             if self.type == "health": color = (255, 0, 0)
             elif self.type == "speed": color = (255, 255, 0)
             elif self.type == "rapid_fire": color = (255, 128, 0)
             pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    def collides_with(self, player):
        return math.hypot(self.x - player.x, self.y - player.y) < self.radius + player.radius

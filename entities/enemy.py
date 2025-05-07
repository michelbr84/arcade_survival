import pygame
import math
from config.settings import screen, RED

class Enemy:
    def __init__(self, x, y, speed=1.5, health=20):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.radius = 15

    def update(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

    def hit(self, bullet):
        return math.hypot(self.x - bullet.x, self.y - bullet.y) < self.radius + bullet.radius

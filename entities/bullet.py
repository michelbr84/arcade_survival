import pygame
from config.settings import screen, WIDTH, HEIGHT, YELLOW

class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = 4
        self.speed = 10

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

    def offscreen(self):
        return not (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT)

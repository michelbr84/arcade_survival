import pygame
import math
from config.settings import screen, WIDTH, HEIGHT, GREEN, RED
from config.paths import get_sound
from entities.bullet import Bullet

class Player:
    def __init__(self):
        self.radius = 15
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 5
        self.health = 100
        self.cooldown = 0

    def move(self, keys):
        dx = dy = 0
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_d]: dx += 1
        length = math.hypot(dx, dy)
        if length != 0:
            dx = dx / length * self.speed
            dy = dy / length * self.speed
        self.x = max(self.radius, min(WIDTH - self.radius, self.x + dx))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y + dy))

    def shoot(self, mouse_pos):
        if self.cooldown == 0:
            dx, dy = mouse_pos[0] - self.x, mouse_pos[1] - self.y
            dist = math.hypot(dx, dy)
            if dist == 0: return None
            dx, dy = dx / dist, dy / dist
            self.cooldown = 15
            shoot_sound = get_sound("shoot")
            if shoot_sound:
                shoot_sound.play()
            return Bullet(self.x, self.y, dx, dy)
        return None

    def update_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius)
        pygame.draw.rect(screen, RED, (10, 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (10, 10, self.health, 10))

    def collides_with(self, other):
        return math.hypot(self.x - other.x, self.y - other.y) < self.radius + other.radius

import pygame
import math
from config.settings import screen, WIDTH, HEIGHT
from config.paths import ENEMY_BULLET_IMG_PATH

class EnemyBullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 4
        self.radius = 8
        self.image = None
        
        try:
            self.image = pygame.image.load(ENEMY_BULLET_IMG_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        except Exception as e:
            print(f"Error loading enemy bullet: {e}")

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self):
        if self.image:
             # Calculate angle for rotation
             angle = math.degrees(math.atan2(-self.dy, self.dx)) - 90
             rotated_image = pygame.transform.rotate(self.image, angle)
             rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
             screen.blit(rotated_image, rect)
        else:
             pygame.draw.circle(screen, (255, 100, 0), (int(self.x), int(self.y)), self.radius)

    def offscreen(self):
        return not (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT)

    def collides_with(self, player):
        return math.hypot(self.x - player.x, self.y - player.y) < self.radius + player.radius

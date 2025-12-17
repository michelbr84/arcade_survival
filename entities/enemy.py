import pygame
import math
import random
from config.settings import screen, RED, BLUE, YELLOW, WHITE, WIDTH, HEIGHT
from entities.enemy_bullet import EnemyBullet

class Enemy:
    def __init__(self, x, y, enemy_type="normal", wave=1, difficulty=None):
        self.x = x
        self.y = y
        self.type = enemy_type
        
        if difficulty is None:
             difficulty = {"hp": 1.0, "speed": 1.0, "damage": 1.0}
        
        # Base stats
        self.speed = (1.5 + wave * 0.1) * difficulty["speed"]
        self.health = (20 + wave * 5) * difficulty["hp"]
        self.radius = 15
        self.damage = 1 * difficulty["damage"]
        
        # Type overrides
        sheet_path = None
        scale_factor = 3
        
        if self.type == "fast":
            self.speed *= 1.8
            self.health *= 0.5
            self.radius = 12
            from config.paths import FAST_ENEMY_SHEET_PATH
            sheet_path = FAST_ENEMY_SHEET_PATH
            scale_factor = 2.5
        elif self.type == "tank":
            self.speed *= 0.6
            self.health *= 3.0
            self.radius = 25
            self.damage = 2
            from config.paths import TANK_ENEMY_SHEET_PATH
            sheet_path = TANK_ENEMY_SHEET_PATH
            scale_factor = 4
        elif self.type == "shooter":
            self.speed *= 0.8
            self.health *= 0.8
            self.radius = 18
            from config.paths import SHOOTER_ENEMY_SHEET_PATH
            sheet_path = SHOOTER_ENEMY_SHEET_PATH
            self.shoot_cooldown = 0
            self.shoot_range = 300
            
        else: # normal
            from config.paths import ENEMY_SHEET_PATH
            sheet_path = ENEMY_SHEET_PATH

        from core.animation import Animation, load_sprite_sheet
        try:
            sheet_surface = pygame.image.load(sheet_path).convert_alpha()
            sheet_w, sheet_h = sheet_surface.get_size()
            frame_w = sheet_w // 4
            frame_h = sheet_h
            frames = load_sprite_sheet(sheet_path, frame_w, frame_h, scale=(self.radius*scale_factor, self.radius*scale_factor))
            self.animation = Animation(frames, 200 if self.type != "fast" else 100)
        except Exception:
            self.animation = None
            self.image = None

    def update(self, player, dt=0, bullets_list=None):
        if self.animation:
            self.animation.update(dt)
            
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        
        if self.type == "shooter":
            if dist < self.shoot_range:
                # Stop and shoot
                if self.shoot_cooldown <= 0:
                    if bullets_list is not None:
                         # Lead the target slightly? No, just direct for now
                         bdx, bdy = dx/dist, dy/dist
                         bullets_list.append(EnemyBullet(self.x, self.y, bdx, bdy))
                         self.shoot_cooldown = 120 # 2 seconds at 60 FPS
                else:
                    self.shoot_cooldown -= 1
            else:
                 # Move towards player
                 if dist != 0:
                    self.x += dx / dist * self.speed
                    self.y += dy / dist * self.speed
        else:
            # Normal chase behavior
            if dist != 0:
                self.x += dx / dist * self.speed
                self.y += dy / dist * self.speed

    def draw(self):
        image_to_draw = None
        if self.animation:
            image_to_draw = self.animation.get_current_frame()
        
        if image_to_draw:
            rect = image_to_draw.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(image_to_draw, rect)
        else:
            color = RED
            if self.type == "fast": color = YELLOW
            elif self.type == "tank": color = BLUE
            elif self.type == "shooter": color = WHITE
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    def hit(self, bullet):
        return math.hypot(self.x - bullet.x, self.y - bullet.y) < self.radius + bullet.radius

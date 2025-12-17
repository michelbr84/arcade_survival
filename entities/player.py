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
        self.max_health = 100
        
        # Buff timers (in ms)
        self.speed_boost_timer = 0
        self.rapid_fire_timer = 0
        from config.paths import PLAYER_SHEET_PATH
        from core.animation import Animation, load_sprite_sheet
        
        # Load sprite sheet: assuming 4 frames, width/height roughly 64x64 or manageable
        # Since I don't know the exact generated size, I'll guess or try to detect.
        # But load_sprite_sheet splits by width. Let's assume the generated image is square-ish frames.
        # Actually, generated images are usually 1024x1024 or similar if not specified.
        # But I asked for a sprite sheet. Let's try to load it and see.
        # Safest bet: load entire image, divide width by 4 to get frame width.
        
        try:
            sheet_surface = pygame.image.load(PLAYER_SHEET_PATH).convert_alpha()
            sheet_w, sheet_h = sheet_surface.get_size()
            frame_w = sheet_w // 4
            frame_h = sheet_h
            frames = load_sprite_sheet(PLAYER_SHEET_PATH, frame_w, frame_h, scale=(self.radius*3, self.radius*3))
            self.animation = Animation(frames, 150) # 150ms per frame
        except Exception as e:
            print(f"Error loading player animation: {e}")
            self.animation = None
            
        # Fallback to single image if animation fails
        if not self.animation:
            from config.paths import get_image
            self.image = get_image("player")
            if self.image:
                self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))

    def update(self, dt):
        self.update_cooldown()
        
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= dt
            
        if self.animation:
            self.animation.update(dt)

    def move(self, keys, axis_input=None):
        dx = dy = 0
        
        # Keyboard Input
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_d]: dx += 1
        
        # Component normalize keyboard
        length = math.hypot(dx, dy)
        if length != 0:
            dx = dx / length
            dy = dy / length
            
        # Joystick Input Override/Add
        if axis_input:
            jx, jy = axis_input
            if abs(jx) > 0.1 or abs(jy) > 0.1: # Deadzone check
                dx = jx
                dy = jy

        # Apply speed and buffs
        final_length = math.hypot(dx, dy)
        if final_length > 1: # Cap at 1.0 for analog sticks to prevent super speed diagonal if unnormalized, though usually sticks are circular.
             dx /= final_length
             dy /= final_length
             
        if dx != 0 or dy != 0:
             current_speed = self.speed * (1.5 if self.speed_boost_timer > 0 else 1.0)
             self.x = max(self.radius, min(WIDTH - self.radius, self.x + dx * current_speed))
             self.y = max(self.radius, min(HEIGHT - self.radius, self.y + dy * current_speed))

    def shoot(self, mouse_pos=None, aim_vector=None):
        if self.cooldown == 0:
            dx = dy = 0
            
            if aim_vector:
                dx, dy = aim_vector
                if math.hypot(dx, dy) < 0.5: return None # Deadzone for stick aiming
            elif mouse_pos:
                dx, dy = mouse_pos[0] - self.x, mouse_pos[1] - self.y
                
            dist = math.hypot(dx, dy)
            if dist == 0: return None
            dx, dy = dx / dist, dy / dist
            self.cooldown = 8 if self.rapid_fire_timer > 0 else 15
            shoot_sound = get_sound("shoot")
            if shoot_sound:
                shoot_sound.play()
            return Bullet(self.x, self.y, dx, dy)
        return None

    def update_cooldown(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def draw(self):
        # Calculate rotation angle
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - self.x, mouse_y - self.y
        angle = math.degrees(math.atan2(-dy, dx)) - 90  # correction for sprite orientation

        image_to_draw = None
        if self.animation:
            image_to_draw = self.animation.get_current_frame()
        elif hasattr(self, 'image') and self.image:
            image_to_draw = self.image

        if image_to_draw:
            rotated_image = pygame.transform.rotate(image_to_draw, angle)
            rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(rotated_image, rect)
        else:
            pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), self.radius)
        
        pygame.draw.rect(screen, RED, (10, 10, 100, 10))
        pygame.draw.rect(screen, GREEN, (10, 10, self.health, 10))

    def collides_with(self, other):
        return math.hypot(self.x - other.x, self.y - other.y) < self.radius + other.radius

from config.settings import screen, WIDTH, HEIGHT, WHITE, BLACK, GREEN, RED, YELLOW, BLUE, GRAY, FPS, clock, RESOLUTIONS, fullscreen, current_res_index, set_volumes
from config.paths import get_sound
from core.utils import draw_text, button, resolve_overlap
from entities.player import Player
from entities.bullet import Bullet
from entities.enemy import Enemy
import pygame
import sys
import random

class Game:
    def __init__(self):
        self.state = "MENU"
        self.paused = False
        self.options = False
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.spawn_timer = 0
        self.score = 0
        self.wave = 1
        self.high_score = 0
        pygame.mixer.music.play(-1)

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_options(self):
        self.options = not self.options

    def reset(self):
        global screen, WIDTH, HEIGHT
        WIDTH, HEIGHT = RESOLUTIONS[current_res_index]
        flags = pygame.FULLSCREEN if fullscreen else 0
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        set_volumes()
        self.__init__()

    def run(self):
        while True:
            screen.fill(BLACK)

            if self.state == "MENU":
                draw_text("ARCADE SURVIVAL", WIDTH//2, HEIGHT//3, YELLOW, center=True)
                draw_text("Press ENTER to Start", WIDTH//2, HEIGHT//2, WHITE, center=True)
                draw_text("Press ESC to Quit", WIDTH//2, HEIGHT//2 + 40, WHITE, center=True)
                for e in pygame.event.get():
                    if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_RETURN: self.state = "GAME"
                        if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

            elif self.state == "GAME":
                self.handle_game_events()
                if self.options:
                    self.show_options_menu()
                elif self.paused:
                    self.show_pause_menu()
                else:
                    self.update_game()

            pygame.display.flip()
            clock.tick(FPS)

    def handle_game_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.options:
                        self.options = False
                    else:
                        self.toggle_pause()
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not self.paused:
                bullet = self.player.shoot(pygame.mouse.get_pos())
                if bullet: self.bullets.append(bullet)

    def update_game(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.player.update_cooldown()
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.offscreen(): self.bullets.remove(bullet)

        self.spawn_timer += 1
        if self.spawn_timer > max(60 - self.wave * 2, 10):
            self.spawn_timer = 0
            ex, ey = random.choice([(random.randint(0, WIDTH), 0), (random.randint(0, WIDTH), HEIGHT), (0, random.randint(0, HEIGHT)), (WIDTH, random.randint(0, HEIGHT))])
            self.enemies.append(Enemy(ex, ey, 1.5 + self.wave * 0.1, 20 + self.wave * 5))

        for enemy in self.enemies[:]:
            enemy.update(self.player)
            for bullet in self.bullets[:]:
                if enemy.hit(bullet):
                    enemy.health -= 10
                    self.bullets.remove(bullet)
                    if enemy.health <= 0:
                        kill_sound = get_sound("kill")
                        if kill_sound: kill_sound.play()
                        self.enemies.remove(enemy)
                        self.score += 100

        for i, a in enumerate(self.enemies):
            for b in self.enemies[i+1:]: resolve_overlap(a, b)
            resolve_overlap(self.player, a)
            if self.player.collides_with(a):
                self.player.health -= 1
                if self.player.health <= 0:
                    self.state = "MENU"
                    gameover_sound = get_sound("gameover")
                    if gameover_sound: gameover_sound.play()

        self.player.draw()
        for bullet in self.bullets: bullet.draw()
        for enemy in self.enemies: enemy.draw()
        draw_text(f"Score: {self.score}", WIDTH - 150, 10)
        draw_text(f"Wave: {self.wave}", WIDTH - 150, 40)
        if pygame.time.get_ticks() // 10000 > self.wave: self.wave += 1

    def show_pause_menu(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        draw_text("PAUSED", WIDTH//2, HEIGHT//3, YELLOW, center=True)
        if button((WIDTH//2-100, HEIGHT//2-60, 200, 40), "Options", mouse, click): self.toggle_options()
        if button((WIDTH//2-100, HEIGHT//2,     200, 40), "Return", mouse, click): self.toggle_pause()
        if button((WIDTH//2-100, HEIGHT//2+60,  200, 40), "Exit",   mouse, click): pygame.quit(); sys.exit()

    def show_options_menu(self):
        global fullscreen, current_res_index
        from config import settings as s
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        draw_text("OPTIONS", WIDTH//2, HEIGHT//5, YELLOW, center=True)
        draw_text(f"Master Volume: {int(s.master_volume*100)}%", WIDTH//2, HEIGHT//5 + 50, WHITE, center=True)
        draw_text(f"Music Volume:  {int(s.music_volume*100)}%", WIDTH//2, HEIGHT//5 + 90, WHITE, center=True)
        draw_text(f"Effects Volume:{int(s.effects_volume*100)}%", WIDTH//2, HEIGHT//5 + 130, WHITE, center=True)
        draw_text(f"Resolution: {RESOLUTIONS[current_res_index][0]}x{RESOLUTIONS[current_res_index][1]}", WIDTH//2, HEIGHT//5 + 170, WHITE, center=True)
        draw_text(f"Fullscreen: {'Yes' if fullscreen else 'No'}", WIDTH//2, HEIGHT//5 + 210, WHITE, center=True)

        if button((WIDTH//2 - 100, HEIGHT//5 + 250, 200, 40), "Back", mouse, click): self.options = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]: s.master_volume = min(1.0, s.master_volume + 0.05)
        if keys[pygame.K_2]: s.master_volume = max(0.0, s.master_volume - 0.05)
        if keys[pygame.K_3]: s.music_volume = min(1.0, s.music_volume + 0.05)
        if keys[pygame.K_4]: s.music_volume = max(0.0, s.music_volume - 0.05)
        if keys[pygame.K_5]: s.effects_volume = min(1.0, s.effects_volume + 0.05)
        if keys[pygame.K_6]: s.effects_volume = max(0.0, s.effects_volume - 0.05)
        if keys[pygame.K_7]:
            current_res_index = (current_res_index + 1) % len(RESOLUTIONS)
        if keys[pygame.K_8]:
            fullscreen = not fullscreen
        set_volumes()
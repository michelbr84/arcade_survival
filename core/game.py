from config.settings import screen, WIDTH, HEIGHT, WHITE, BLACK, GREEN, RED, YELLOW, BLUE, GRAY, FPS, clock, RESOLUTIONS, fullscreen, current_res_index, set_volumes
from config.paths import get_sound
from core.utils import draw_text, button, resolve_overlap
from core.score_manager import get_highest_score, save_highscore
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
        self.player_dead = False
        self.bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.enemies = []
        self.spawn_timer = 0
        self.score = 0
        self.wave = 1
        self.high_score = get_highest_score()
        pygame.mixer.music.play(-1)
        
        # Joystick Initialization
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick initialized: {self.joystick.get_name()}")
            
        # UI Sliders (Initialized on demand or here? Here is safer)
        from config import settings as s
        # x, y, w, h, min, max, val
        # Positions will be dynamic based on resolution, so maybe init in show_options?
        # But we want state persistence during the frame.
        # Let's just create them in __init__ with placeholder positions or update them in show_options loop?
        # Better: create them in show_options_menu if they don't exist, or just recreate them effectively?
        # To keep state (dragging), we need them to persist across frames of the menu loop.
        self.sliders = None

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_options(self):
        self.options = not self.options

    def reset(self):
        global screen, WIDTH, HEIGHT, fullscreen
        WIDTH, HEIGHT = RESOLUTIONS[current_res_index]
        flags = pygame.FULLSCREEN if fullscreen else 0
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        set_volumes()
        self.__init__() # Re-initialize game state

    def handle_gameover_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

    def show_game_over_menu(self):
        from core.menus import show_game_over_screen
        action = show_game_over_screen(self.score, self.high_score)
        if action == "RETRY":
            self.reset()
            self.state = "GAME"
        elif action == "MENU":
            self.reset()
            self.state = "MENU"

    def run(self):
        while True:
            screen.fill(BLACK)

            if self.state == "MENU":
                draw_text("ARCADE SURVIVAL", WIDTH//2, HEIGHT//3 - 40, YELLOW, center=True)
                
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()[0]
                
                if button((WIDTH//2 - 100, HEIGHT//2, 200, 40), "Start Game", mouse, click):
                    self.state = "GAME"
                
                if button((WIDTH//2 - 100, HEIGHT//2 + 60, 200, 40), "Leaderboard", mouse, click):
                    self.state = "LEADERBOARD"
                    
                if button((WIDTH//2 - 100, HEIGHT//2 + 120, 200, 40), "Quit", mouse, click):
                    pygame.quit()
                    sys.exit()
                    
                draw_text(f"High Score: {self.high_score}", WIDTH//2, HEIGHT//10, GRAY, center=True)

                for e in pygame.event.get():
                    if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                    elif e.type == pygame.KEYDOWN:
                         if e.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

            elif self.state == "GAME":
                self.handle_game_events()
                if self.options:
                    self.show_options_menu()
                elif self.paused:
                    self.show_pause_menu()
                else:
                    self.update_game()

            elif self.state == "GAMEOVER":
                self.handle_gameover_events()
                self.show_game_over_menu()
                
            elif self.state == "LEADERBOARD":
                self.handle_gameover_events() # Re-use generic event handler or make new one? 
                # Generic just checks quit.
                from core.menus import show_leaderboard_screen
                from core.score_manager import get_leaderboard
                action = show_leaderboard_screen(get_leaderboard())
                if action == "BACK":
                    self.state = "MENU"

            pygame.display.flip()

            pygame.display.flip()
            pygame.display.flip()
            self.dt = clock.tick(FPS)
            
    def handle_game_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.options:
                        self.options = False
                    else:
                        self.toggle_pause()
            elif e.type == pygame.JOYBUTTONDOWN:
                 if e.button == 7: # Start button usually
                     self.toggle_pause()
            
            # Mouse shooting
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not self.paused:
                bullet = self.player.shoot(mouse_pos=pygame.mouse.get_pos())
                if bullet: self.bullets.append(bullet)

    def update_game(self):
        keys = pygame.key.get_pressed()
        
        # Joystick Axis
        axis_move = None
        aim_vec = None
        if self.joystick:
            # Left stick (0, 1)
            axis_move = (self.joystick.get_axis(0), self.joystick.get_axis(1))
            # Right stick (2, 3) or (3, 4) depending on OS/Controller. Usually 2, 3 or 3, 4. 
            # Xbox on Windows: 0=LX, 1=LY, 2=RX, 3=RY OR 2=Trigger, 3=RY, 4=RX. 
            # Pygame 2 usually mapping: 0=LX, 1=LY, 2=RX, 3=RY (if triggers are axes 4/5)
            # Let's try 2 and 3 for now.
            rx = self.joystick.get_axis(2)
            ry = self.joystick.get_axis(3)
            # Some controllers use 3 and 4.
            if abs(rx) < 0.1 and abs(ry) < 0.1 and self.joystick.get_numaxes() >= 5:
                 rx = self.joystick.get_axis(3)
                 ry = self.joystick.get_axis(4)

            aim_vec = (rx, ry)
            
            # Auto-fire on right stick stick movement
            if math.hypot(rx, ry) > 0.5:
                bullet = self.player.shoot(aim_vector=(rx, ry))
                if bullet: self.bullets.append(bullet)

        self.player.move(keys, axis_input=axis_move)
        self.player.update(self.dt) # Renamed or added dt support
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.offscreen(): self.bullets.remove(bullet)
            
        for eb in self.enemy_bullets[:]:
            eb.update()
            if eb.offscreen(): self.enemy_bullets.remove(eb)
            elif eb.collides_with(self.player):
                self.player.health -= 5 # Bullet damage
                self.enemy_bullets.remove(eb)
                if self.player.health <= 0 and not self.player_dead:
                    self.player_dead = True
                    self.state = "GAMEOVER"
                    gameover_sound = get_sound("gameover")
                    if gameover_sound: gameover_sound.play()
                    save_highscore("Survivor", self.score)
                    if self.score > self.high_score:
                         self.high_score = self.score

        self.spawn_timer += 1
        
        from config.settings import DIFFICULTY, current_difficulty
        diff_settings = DIFFICULTY[current_difficulty]
        spawn_rate_mult = diff_settings["spawn_rate"]
        
        if self.spawn_timer > max((60 - self.wave * 2) * spawn_rate_mult, 10):
            self.spawn_timer = 0
            ex, ey = random.choice([(random.randint(0, WIDTH), 0), (random.randint(0, WIDTH), HEIGHT), (0, random.randint(0, HEIGHT)), (WIDTH, random.randint(0, HEIGHT))])
            
            # Weighted random spawn
            r = random.random()
            etype = "normal"
            if self.wave > 2 and r < 0.2: etype = "fast"
            elif self.wave > 3 and r < 0.4: etype = "tank"
            elif self.wave > 4 and r < 0.6: etype = "shooter"
            
            self.enemies.append(Enemy(ex, ey, etype, self.wave, diff_settings))

        for enemy in self.enemies[:]:
            enemy.update(self.player, self.dt, self.enemy_bullets)
            for bullet in self.bullets[:]:
                if enemy.hit(bullet):
                    enemy.health -= 10
                    self.bullets.remove(bullet)
                    if enemy.health <= 0:
                        kill_sound = get_sound("kill")
                        if kill_sound: kill_sound.play()
                        
                        # Loot Drop / Power-up
                        if random.random() < 0.2: # 20% chance
                             from entities.powerup import PowerUp
                             ptype = random.choice(["health"]*5 + ["speed"]*3 + ["rapid_fire"]*2)
                             self.powerups.append(PowerUp(enemy.x, enemy.y, ptype))
                        
                        self.enemies.remove(enemy)
                        self.score += 100 * (2 if enemy.type=="tank" else 1.5 if enemy.type=="shooter" else 1)
        
        # Powerups update and collision
        for p in self.powerups[:]:
            p.update()
            if p.life_time <= 0:
                self.powerups.remove(p)
            elif p.collides_with(self.player):
                if p.type == "health":
                    self.player.health = min(self.player.max_health, self.player.health + 20)
                elif p.type == "speed":
                    self.player.speed_boost_timer = 5000 # 5 seconds
                elif p.type == "rapid_fire":
                    self.player.rapid_fire_timer = 5000 # 5 seconds
                self.powerups.remove(p)

        for i, a in enumerate(self.enemies):
            for b in self.enemies[i+1:]: resolve_overlap(a, b)
            resolve_overlap(self.player, a)
            if self.player.collides_with(a):
                self.player.health -= 1
                if self.player.health <= 0 and not self.player_dead:
                    self.player_dead = True
                    self.state = "GAMEOVER"
                    gameover_sound = get_sound("gameover")
                    if gameover_sound: gameover_sound.play()
                    save_highscore("Survivor", self.score)
                    if self.score > self.high_score:
                         self.high_score = self.score

        self.player.draw()
        for bullet in self.bullets: bullet.draw()
        for eb in self.enemy_bullets: eb.draw()
        for p in self.powerups: p.draw()
        for enemy in self.enemies: enemy.draw()
        draw_text(f"Score: {self.score}", WIDTH - 150, 10)
        draw_text(f"High Score: {max(self.score, self.high_score)}", WIDTH - 150, 30, color=GRAY)
        draw_text(f"Wave: {self.wave}", WIDTH - 150, 60)
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
        from core.utils import Slider
        
        if self.sliders is None:
            # Init sliders relative to center
            cx = WIDTH // 2
            cy = HEIGHT // 5
            self.sliders = {
                "master": Slider(cx - 100, cy + 60, 200, 20, 0.0, 1.0, s.master_volume),
                "music": Slider(cx - 100, cy + 100, 200, 20, 0.0, 1.0, s.music_volume),
                "effects": Slider(cx - 100, cy + 140, 200, 20, 0.0, 1.0, s.effects_volume)
            }

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        
        draw_text("OPTIONS", WIDTH//2, HEIGHT//5, YELLOW, center=True)
        
        # Sliders
        draw_text(f"Master Volume: {int(s.master_volume*100)}%", WIDTH//2, HEIGHT//5 + 40, WHITE, center=True)
        self.sliders["master"].draw(screen)
        if self.sliders["master"].update(mouse, click):
            s.master_volume = self.sliders["master"].value
            
        draw_text(f"Music Volume:  {int(s.music_volume*100)}%", WIDTH//2, HEIGHT//5 + 80, WHITE, center=True)
        self.sliders["music"].draw(screen)
        if self.sliders["music"].update(mouse, click):
            s.music_volume = self.sliders["music"].value
            
        draw_text(f"Effects Volume:{int(s.effects_volume*100)}%", WIDTH//2, HEIGHT//5 + 120, WHITE, center=True)
        self.sliders["effects"].draw(screen)
        if self.sliders["effects"].update(mouse, click):
            s.effects_volume = self.sliders["effects"].value

        draw_text(f"Resolution: {RESOLUTIONS[current_res_index][0]}x{RESOLUTIONS[current_res_index][1]}", WIDTH//2, HEIGHT//5 + 170, WHITE, center=True)
        draw_text(f"Fullscreen: {'Yes' if fullscreen else 'No'}", WIDTH//2, HEIGHT//5 + 210, WHITE, center=True)
        draw_text(f"Difficulty: {s.current_difficulty}", WIDTH//2, HEIGHT//5 + 250, WHITE, center=True)

        if button((WIDTH//2 - 100, HEIGHT//5 + 290, 200, 40), "Back", mouse, click):
             self.options = False
             self.sliders = None # Reset sliders so they re-center if res changes? Or keep them. Reseting is safer for layout.

        keys = pygame.key.get_pressed()
        if keys[pygame.K_7]:
            current_res_index = (current_res_index + 1) % len(RESOLUTIONS)
            # Reset sliders on res change to recompute positions
            self.sliders = None
            # Small delay to prevent rapid toggle
            pygame.time.wait(200)
            
        if keys[pygame.K_8]:
            fullscreen = not fullscreen
            self.sliders = None
            pygame.time.wait(200)
            
        if keys[pygame.K_9]:
             diff_keys = list(s.DIFFICULTY.keys())
             curr_idx = diff_keys.index(s.current_difficulty)
             s.current_difficulty = diff_keys[(curr_idx + 1) % len(diff_keys)]
             pygame.time.wait(200)
             
        set_volumes()

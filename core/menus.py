import pygame
import sys
from config.settings import WIDTH, HEIGHT, YELLOW, WHITE, screen
from core.utils import draw_text, button


def show_main_menu():
    screen.fill((0, 0, 0))
    draw_text("ARCADE SURVIVAL", WIDTH // 2, HEIGHT // 3, YELLOW, center=True)
    draw_text("Press ENTER to Start", WIDTH // 2, HEIGHT // 2, WHITE, center=True)
    draw_text("Press ESC to Quit", WIDTH // 2, HEIGHT // 2 + 40, WHITE, center=True)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "GAME"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def show_pause_menu(toggle_pause_callback, toggle_options_callback):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]
    draw_text("PAUSED", WIDTH // 2, HEIGHT // 3, YELLOW, center=True)
    if button((WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 40), "Options", mouse, click):
        toggle_options_callback()
    if button((WIDTH // 2 - 100, HEIGHT // 2, 200, 40), "Return", mouse, click):
        toggle_pause_callback()
    if button((WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 40), "Exit", mouse, click):
        pygame.quit()
        sys.exit()


def show_options_menu(settings_module):
    from config.settings import RESOLUTIONS, current_res_index, fullscreen, set_volumes

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    draw_text("OPTIONS", WIDTH // 2, HEIGHT // 5, YELLOW, center=True)
    draw_text(f"Master Volume: {int(settings_module.master_volume * 100)}%", WIDTH // 2, HEIGHT // 5 + 50, WHITE, center=True)
    draw_text(f"Music Volume:  {int(settings_module.music_volume * 100)}%", WIDTH // 2, HEIGHT // 5 + 90, WHITE, center=True)
    draw_text(f"Effects Volume:{int(settings_module.effects_volume * 100)}%", WIDTH // 2, HEIGHT // 5 + 130, WHITE, center=True)
    draw_text(f"Resolution: {RESOLUTIONS[current_res_index][0]}x{RESOLUTIONS[current_res_index][1]}", WIDTH // 2, HEIGHT // 5 + 170, WHITE, center=True)
    draw_text(f"Fullscreen: {'Yes' if fullscreen else 'No'}", WIDTH // 2, HEIGHT // 5 + 210, WHITE, center=True)

    if button((WIDTH // 2 - 100, HEIGHT // 5 + 250, 200, 40), "Back", mouse, click):
        return False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]: settings_module.master_volume = min(1.0, settings_module.master_volume + 0.05)
    if keys[pygame.K_2]: settings_module.master_volume = max(0.0, settings_module.master_volume - 0.05)
    if keys[pygame.K_3]: settings_module.music_volume = min(1.0, settings_module.music_volume + 0.05)
    if keys[pygame.K_4]: settings_module.music_volume = max(0.0, settings_module.music_volume - 0.05)
    if keys[pygame.K_5]: settings_module.effects_volume = min(1.0, settings_module.effects_volume + 0.05)
    if keys[pygame.K_6]: settings_module.effects_volume = max(0.0, settings_module.effects_volume - 0.05)
    if keys[pygame.K_7]:
        settings_module.current_res_index = (settings_module.current_res_index + 1) % len(RESOLUTIONS)
    if keys[pygame.K_8]:
        settings_module.fullscreen = not settings_module.fullscreen

    set_volumes()
    return True

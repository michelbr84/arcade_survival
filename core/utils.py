import pygame
import math
from config.settings import font, screen, WHITE, GRAY, BLUE, BLACK


def draw_text(text, x, y, color=WHITE, center=False):
    """
    Renders text on screen at a given position. If center=True, centers it.
    """
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    rect.center = (x, y) if center else (x, y)
    screen.blit(surface, rect)


def button(rect, text, mouse_pos, click, color=GRAY, hover_color=BLUE):
    """
    Creates an interactive button that reacts to mouse hover and click.
    """
    p_rect = pygame.Rect(rect)
    is_hovered = p_rect.collidepoint(mouse_pos)
    pygame.draw.rect(screen, color, p_rect, border_radius=5)
    # The original instruction had `x + w // 2, y + h // 2, BLACK` which are undefined.
    # Assuming the intent was to center the text within the button rect.
    draw_text(text, p_rect.centerx, p_rect.centery, BLACK, center=True)
    return is_hovered and click


def resolve_overlap(a, b):
    """
    Resolves physical overlap between two circular entities (like player and enemies).
    """
    dx = b.x - a.x
    dy = b.y - a.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        dx, dy, dist = 1, 0, 1
    min_dist = a.radius + b.radius
    if dist < min_dist:
        overlap = min_dist - dist
        shift_x = dx / dist * overlap / 2
        shift_y = dy / dist * overlap / 2
        b.x += shift_x
        b.y += shift_y
        a.x -= shift_x
        a.y -= shift_y

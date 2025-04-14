import pygame
from config import *

def draw_menu(screen, selected_difficulty, road_image):
    screen.blit(road_image, (0, 0))
    font = pygame.font.SysFont(None, 55)
    title = font.render("Frogger Clone", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    difficulties = ["easy", "medium", "hard"]
    buttons = []
    for i, diff in enumerate(difficulties):
        color = WHITE if diff == selected_difficulty else (150, 150, 150)
        text = font.render(diff.capitalize(), True, color)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 100))
        buttons.append((rect, diff))
        screen.blit(text, rect)

    start_text = font.render("Press ENTER to Start", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 500))
    return buttons

def draw_pause_menu(screen, selected_option):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))

    font = pygame.font.SysFont(None, 55)
    title = font.render("Paused", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

    options = ["Resume", "Exit"]
    buttons = []
    for i, option in enumerate(options):
        color = WHITE if option == selected_option else (150, 150, 150)
        text = font.render(option, True, color)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 100))
        buttons.append((rect, option))
        screen.blit(text, rect)

    return buttons
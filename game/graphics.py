import pygame
import os
import sys
from config import *

def load_images():
    car_images = []
    try:
        frog_img = pygame.image.load("images/frog.png").convert_alpha()
        frog_img = pygame.transform.scale(frog_img, (FROG_SIZE, FROG_SIZE))
        for file in os.listdir("images"):
            if file.startswith("car") and file.endswith(".png"):
                img = pygame.image.load(os.path.join("images", file)).convert_alpha()
                img_width, img_height = img.get_size()
                scale = min(GRID_SIZE / img_width, GRID_SIZE / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                img = pygame.transform.scale(img, (new_width, new_height))
                car_images.append(img)
        road_img = pygame.image.load("images/road.png").convert_alpha()
        road_img = pygame.transform.scale(road_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading images: {e}")
        print(
            "Please ensure frog.png, car*.png, and road.png are in the images/ folder."
        )
        pygame.quit()
        sys.exit()

    if not car_images:
        print("No car images found. Ensure files are named car1.png, car2.png, etc.")
        pygame.quit()
        sys.exit()

    return frog_img, car_images, road_img

def draw_game(screen, road_image, frog, cars, game_over, won, frog_image):
    screen.blit(road_image, (0, 0))
    for car in cars:
        car.draw(screen)
    frog.draw(screen, frog_image)

    font_sub = pygame.font.SysFont(None, 40)
    pulse = 5 * abs((pygame.time.get_ticks() // 100 % 10) - 5)

    if game_over:
        game_over_font = pygame.font.SysFont(None, 80 + pulse)
        game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
        restart_text = font_sub.render(
            "Press R to Restart, ESC to return to Menu", True, WHITE
        )
        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        )
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)

    elif won:
        win_font = pygame.font.SysFont(None, 80 + pulse)
        win_text = win_font.render("You Win!", True, (0, 255, 0))
        restart_text = font_sub.render(
            "Press R to Restart, ESC to return to Menu", True, WHITE
        )
        win_rect = win_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        )
        restart_rect = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        )
        screen.blit(win_text, win_rect)
        screen.blit(restart_text, restart_rect)
import pygame
import sys
from config import *
from entities import Frog, Car
from game_logic import initialize_game, check_collisions, check_win
from graphics import load_images, draw_game
from menu import draw_menu, draw_pause_menu

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frogger Clone")
clock = pygame.time.Clock()

# Load images
try:
    frog_image, car_images, road_image = load_images()
except SystemExit:
    sys.exit()

def main():
    state = "menu"
    selected_difficulty = "medium"
    frog = None
    cars = []
    game_over = False
    won = False
    paused = False
    selected_pause_option = "Resume"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if state == "menu":
                    if event.key == pygame.K_UP:
                        difficulties = ["easy", "medium", "hard"]
                        idx = difficulties.index(selected_difficulty)
                        selected_difficulty = difficulties[(idx - 1) % len(difficulties)]
                    elif event.key == pygame.K_DOWN:
                        difficulties = ["easy", "medium", "hard"]
                        idx = difficulties.index(selected_difficulty)
                        selected_difficulty = difficulties[(idx + 1) % len(difficulties)]
                    elif event.key == pygame.K_RETURN:
                        state = "game"
                        frog, cars = initialize_game(selected_difficulty, car_images)  # Fixed: Added car_images
                        game_over = False
                        won = False
                        paused = False
                elif state == "game":
                    if paused:
                        if event.key == pygame.K_UP:
                            options = ["Resume", "Exit"]
                            idx = options.index(selected_pause_option)
                            selected_pause_option = options[(idx - 1) % len(options)]
                        elif event.key == pygame.K_DOWN:
                            options = ["Resume", "Exit"]
                            idx = options.index(selected_pause_option)
                            selected_pause_option = options[(idx + 1) % len(options)]
                        elif event.key == pygame.K_RETURN:
                            if selected_pause_option == "Resume":
                                paused = False
                            elif selected_pause_option == "Exit":
                                state = "menu"
                                paused = False
                        elif event.key == pygame.K_ESCAPE:
                            paused = False
                    else:
                        if event.key == pygame.K_ESCAPE and not game_over and not won:
                            paused = True
                            selected_pause_option = "Resume"
                        elif not game_over and not won:
                            if event.key == pygame.K_UP:
                                frog.move(0, -1)
                            elif event.key == pygame.K_DOWN:
                                frog.move(0, 1)
                            elif event.key == pygame.K_LEFT:
                                frog.move(-1, 0)
                            elif event.key == pygame.K_RIGHT:
                                frog.move(1, 0)
                        if event.key == pygame.K_r and (game_over or won):
                            frog, cars = initialize_game(selected_difficulty, car_images)  # Fixed: Added car_images
                            game_over = False
                            won = False
                        elif event.key == pygame.K_ESCAPE and (game_over or won):
                            state = "menu"

        if state == "menu":
            draw_menu(screen, selected_difficulty, road_image)
            pygame.display.flip()
            clock.tick(60)
            continue

        if paused:
            draw_game(screen, road_image, frog, cars, game_over, won, frog_image)
            draw_pause_menu(screen, selected_pause_option)
            pygame.display.flip()
            clock.tick(60)
            continue

        if not game_over and not won:
            for car in cars:
                car.move()
            game_over = check_collisions(frog, cars)
            won = check_win(frog)

        draw_game(screen, road_image, frog, cars, game_over, won, frog_image)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
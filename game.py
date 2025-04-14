import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 50
GRID_WIDTH = 16
GRID_HEIGHT = 12
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_HEIGHT
FROG_SIZE = GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Frogger Clone")
clock = pygame.time.Clock()

# Load images
def load_images():
    car_images = []
    try:
        frog_img = pygame.image.load("frog3.png").convert_alpha()
        frog_img = pygame.transform.scale(frog_img, (FROG_SIZE, FROG_SIZE))
        for file in os.listdir():
            if file.startswith("car") and file.endswith(".png"):
                img = pygame.image.load(file).convert_alpha()
                img_width, img_height = img.get_size()
                scale = min(GRID_SIZE / img_width, GRID_SIZE / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                img = pygame.transform.scale(img, (new_width, new_height))
                car_images.append(img)
        road_img = pygame.image.load("road3.png").convert_alpha()
        road_img = pygame.transform.scale(road_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading images: {e}")
        print("Please ensure frog.png, car*.png, and road.png are in the same folder as this script.")
        pygame.quit()
        sys.exit()

    if not car_images:
        print("No car images found. Ensure files are named car1.png, car2.png, etc.")
        pygame.quit()
        sys.exit()

    return frog_img, car_images, road_img

frog_image, car_images, road_image = load_images()

# Frog class
class Frog:
    def __init__(self):
        self.x = GRID_WIDTH // 2 * GRID_SIZE
        self.y = (GRID_HEIGHT - 1) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, FROG_SIZE, FROG_SIZE)
        self.direction = "up"

    def move(self, dx, dy):
        new_x = self.x + dx * GRID_SIZE
        new_y = self.y + dy * GRID_SIZE
        if 0 <= new_x < SCREEN_WIDTH and 0 <= new_y < SCREEN_HEIGHT:
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (self.x, self.y)
            if dx == 1:
                self.direction = "right"
            elif dx == -1:
                self.direction = "left"
            elif dy == -1:
                self.direction = "up"
            elif dy == 1:
                self.direction = "down"

    def draw(self):
        rotation_angles = {
            "up": 0,
            "right": -90,
            "down": 180,
            "left": 90
        }
        angle = rotation_angles[self.direction]
        rotated_frog = pygame.transform.rotate(frog_image, angle)
        rotated_rect = rotated_frog.get_rect(center=self.rect.center)
        screen.blit(rotated_frog, rotated_rect)

# Car class
class Car:
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        base_image = random.choice(car_images)
        self.image = pygame.transform.rotate(base_image, -90 if direction == 1 else 90)
        img_width, img_height = self.image.get_size()
        self.rect = pygame.Rect(x, y + (GRID_SIZE - img_height) // 2, img_width, img_height)

    def move(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x
        if self.direction == 1 and self.x > SCREEN_WIDTH:
            self.x = -self.rect.width
        elif self.direction == -1 and self.x < -self.rect.width:
            self.x = SCREEN_WIDTH
        self.rect.x = self.x

    def draw(self):
        screen.blit(self.image, self.rect)

# Initialize game objects
def initialize_game(difficulty):
    frog = Frog()
    speed_multipliers = {"easy": 0.5, "medium": 0.6, "hard": 0.75}
    cars_per_lane = {"easy": 2, "medium": 3, "hard": 4}
    multiplier = speed_multipliers[difficulty]
    num_cars = cars_per_lane[difficulty]
    cars = []
    lanes = [
        (3, 5, 1),
        (4, 6, -1),
        (5, 4, 1),
        (6, 7, -1),
        (7, 5, 1),
    ]
    for row, base_speed, direction in lanes:
        x_positions = list(range(0, SCREEN_WIDTH, GRID_SIZE * 2))
        random.shuffle(x_positions)
        for i in range(num_cars):
            if x_positions:
                x = x_positions.pop()
                cars.append(Car(x, row * GRID_SIZE, base_speed * multiplier, direction))
    return frog, cars

# Main menu
def draw_menu(selected_difficulty):
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

# Pause menu
def draw_pause_menu(selected_option):
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

# Game state
state = "menu"
selected_difficulty = "medium"
frog = None
cars = []
game_over = False
won = False
paused = False
selected_pause_option = "Resume"

# Main game loop
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
                    frog, cars = initialize_game(selected_difficulty)
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
                        frog, cars = initialize_game(selected_difficulty)
                        game_over = False
                        won = False
                    elif event.key == pygame.K_ESCAPE and (game_over or won):
                        state = "menu"

    if state == "menu":
        buttons = draw_menu(selected_difficulty)
        pygame.display.flip()
        clock.tick(60)
        continue

    if paused:
        screen.blit(road_image, (0, 0))
        for car in cars:
            car.draw()
        frog.draw()
        draw_pause_menu(selected_pause_option)
        pygame.display.flip()
        clock.tick(60)
        continue

    if not game_over and not won:
        for car in cars:
            car.move()
        for car in cars:
            if frog.rect.colliderect(car.rect):
                game_over = True
                break
        if frog.y == 0:
            won = True

    screen.blit(road_image, (0, 0))
    for car in cars:
        car.draw()
    frog.draw()

    # Animated game over / win messages
    font_sub = pygame.font.SysFont(None, 40)
    pulse = 5 * abs((pygame.time.get_ticks() // 100 % 10) - 5)

    if game_over:
        game_over_font = pygame.font.SysFont(None, 80 + pulse)
        game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
        restart_text = font_sub.render("Press R to Restart, ESC to return to Menu", True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)

    elif won:
        win_font = pygame.font.SysFont(None, 80 + pulse)
        win_text = win_font.render("You Win!", True, (0, 255, 0))
        restart_text = font_sub.render("Press R to Restart, ESC to return to Menu", True, WHITE)

        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

        screen.blit(win_text, win_rect)
        screen.blit(restart_text, restart_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

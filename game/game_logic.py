import random
from entities import Frog, Car
from config import *

def initialize_game(difficulty, car_images):
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
                cars.append(Car(x, row * GRID_SIZE, base_speed * multiplier, direction, car_images))
    return frog, cars

def check_collisions(frog, cars):
    for car in cars:
        if frog.rect.colliderect(car.rect):
            return True
    return False

def check_win(frog):
    return frog.y == 0
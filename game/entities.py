import pygame
import random
from config import *

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

    def draw(self, screen, frog_image):
        rotation_angles = {"up": 0, "right": -90, "down": 180, "left": 90}
        angle = rotation_angles[self.direction]
        rotated_frog = pygame.transform.rotate(frog_image, angle)
        rotated_rect = rotated_frog.get_rect(center=self.rect.center)
        screen.blit(rotated_frog, rotated_rect)

class Car:
    def __init__(self, x, y, speed, direction, car_images):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        base_image = random.choice(car_images)
        self.image = pygame.transform.rotate(base_image, -90 if direction == 1 else 90)
        img_width, img_height = self.image.get_size()
        self.rect = pygame.Rect(
            x, y + (GRID_SIZE - img_height) // 2, img_width, img_height
        )

    def move(self):
        self.x += self.speed * self.direction
        self.rect.x = self.x
        if self.direction == 1 and self.x > SCREEN_WIDTH:
            self.x = -self.rect.width
        elif self.direction == -1 and self.x < -self.rect.width:
            self.x = SCREEN_WIDTH
        self.rect.x = self.x

    def draw(self, screen):
        screen.blit(self.image, self.rect)
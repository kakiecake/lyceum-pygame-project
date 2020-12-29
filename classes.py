import pygame
import os
import sys
import random
from framework import event_handler, main

balls_group = pygame.sprite.Group()
bricks_group = pygame.sprite.Group()
boards_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print("Файл не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(balls_group, all_sprites)
        self.image = load_image("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, -1)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

    def render(self):
        pass


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(bricks_group, all_sprites)
        self.image = load_image("brick.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        pass

    def render(self):
        pass


class Board(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(boards_group, all_sprites)
        self.image = load_image("board.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    @event_handler(pygame.KEYDOWN, use_event=True)
    def update(self, event):
        if event.key == pygame.K_LEFT:
            self.rect = self.rect.move(-5, 0)
        elif event.key == pygame.K_RIGHT:
            self.rect = self.rect.move(5, 0)

    def render(self):
        pass

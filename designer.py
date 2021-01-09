import pygame
import os
import sys
from framework import event_handler


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print("Файл не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Designer:
    def __init__(self):
        self.bricks_group = pygame.sprite.Group()
        self.bricks = []

    def update(self):
        pass

    def render(self, screen):
        self.bricks_group.draw(screen)

    @event_handler(pygame.MOUSEBUTTONDOWN, use_event=True)
    def mouse_click(self, event):
        if event.button == 1:
            brick = Brick(event.pos)
            if not(pygame.sprite.spritecollideany(brick, self.bricks_group)) and event.pos[0] < 850 and \
                    event.pos[1] < 470:
                self.bricks.append(event.pos)
                self.bricks_group.add(brick)
        elif event.button == 3:
            for brick in self.bricks_group:
                if brick.rect.collidepoint(event.pos):
                    brick.kill()


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("brick.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

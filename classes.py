import pygame
import os
import sys
import random
from framework import event_handler


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print("Файл не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Board:
    def __init__(self, size):
        width, height = size
        self.balls_group = pygame.sprite.Group()
        self.bricks_group = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.horizontal_barriers = pygame.sprite.Group()
        self.vertical_barriers = pygame.sprite.Group()
        self.horizontal_barriers.add(Barrier(0, 0, width, 0))
        self.horizontal_barriers.add(Barrier(0, height, width, height))
        self.vertical_barriers.add(Barrier(0, 0, 0, height))
        self.vertical_barriers.add(Barrier(width, 0, width, height))
        self.platform = Platform((400, 470))
        self.platforms_group.add(self.platform)
        self.bricks_group.add(*[Brick((5 + 105 * i, 5 + 35 * j)) for i in range(10)
                           for j in range(4)])
        self.ball = Ball((random.randint(0, 930), 450))
        self.balls_group.add(self.ball)

    def update(self):
        self.ball.update()
        if pygame.sprite.spritecollideany(self.ball, self.horizontal_barriers):
            self.ball.on_horizontal_collision()
        if pygame.sprite.spritecollideany(self.ball, self.vertical_barriers):
            self.ball.on_vertical_collision()
        for brick in self.bricks_group:
            if pygame.sprite.spritecollideany(brick, self.balls_group):
                pygame.sprite.spritecollide(self.ball, self.bricks_group, True)
                self.ball.on_brick_collision(brick)
                break
        for platform1 in self.platforms_group:
            if pygame.sprite.spritecollideany(platform1, self.balls_group):
                self.ball.on_brick_collision(platform1)

    def render(self, screen):
        self.balls_group.draw(screen)
        self.bricks_group.draw(screen)
        self.platforms_group.draw(screen)

    @event_handler(pygame.KEYDOWN, use_event=True)
    def on_keydown(self, event):
        if event.key == pygame.K_LEFT:
            self.platform.move_left()
        elif event.key == pygame.K_RIGHT:
            self.platform.move_right()

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, -1)
        while self.vx == 0:
            self.vx = random.randint(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

    def on_brick_collision(self, sprite):
        if self.vx > 0:
            x = self.rect.right - sprite.rect.left
        else:
            x = sprite.rect.right - self.rect.left
        if self.vy > 0:
            y = self.rect.bottom - sprite.rect.top
        else:
            y = sprite.rect.bottom - self.rect.top
        if abs(x - y) < 5:
            self.vx, self.vy = -self.vx, -self.vy
        elif x > y:
            self.vy = -self.vy
        elif y > x:
            self.vx = -self.vx

    def on_vertical_collision(self):
        self.vx = -self.vx

    def on_horizontal_collision(self):
        self.vy = -self.vy


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("brick.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        pass


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("platform.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        pass

    def move_left(self):
        self.rect = self.rect.move(-10, 0)

    def move_right(self):
        self.rect = self.rect.move(10, 0)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
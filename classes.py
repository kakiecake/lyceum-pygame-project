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
        self.dead_barriers = pygame.sprite.Group()
        self.gameover_group = pygame.sprite.Group()
        self.hearts_group = pygame.sprite.Group()
        self.hearts_group.add(Heart((55, 5)))
        self.hearts_group.add(Heart((30, 5)))
        self.hearts_group.add(Heart((5, 5)))
        self.gameover = GameOver()
        self.gameover_group.add(self.gameover)
        self.horizontal_barriers.add(Barrier(0, 0, width, 0))
        self.dead_barriers.add(Barrier(0, height - 20, width, height - 20))
        self.vertical_barriers.add(Barrier(0, 0, 0, height))
        self.vertical_barriers.add(Barrier(width, 0, width, height))
        self.platform = Platform((400, 470), width)
        self.platforms_group.add(self.platform)
        self.bricks_group.add(*[Brick((5 + 105 * i, 5 + 35 * j)) for i in range(9)
                                for j in range(1)])
        self.ball = Ball((random.randint(0, 930), 450))
        self.balls_group.add(self.ball)
        self.life = 2
        self.end_game = False

    def update(self):
        if self.end_game is False:
            pygame.mouse.set_visible(False)
            self.ball.update()
            if pygame.sprite.spritecollideany(self.ball, self.dead_barriers):
                self.ball.die()
                for heart in self.hearts_group:
                    heart.kill()
                    break
                if self.life < 1:
                    self.end()
                else:
                    self.life -= 1
                    self.ball = Ball((random.randint(0, 930), 450))
                    self.balls_group.add(self.ball)
            if len(self.bricks_group.sprites()) == 0:
                self.end()
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
        else:
            self.gameover.update()

    def render(self, screen):
        self.balls_group.draw(screen)
        self.bricks_group.draw(screen)
        self.platforms_group.draw(screen)
        self.gameover_group.draw(screen)
        self.hearts_group.draw(screen)

    @event_handler(pygame.MOUSEMOTION, use_event=True)
    def on_move_mouse(self, event):
        self.platform.move(event.pos)

    def end(self):
        self.end_game = True


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-10, -1)
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

    def die(self):
        self.kill()


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("brick.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, width):
        super().__init__()
        self.image = load_image("platform.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.x = pos[0] + 75
        self.width = width

    def move(self, pos):
        self.rect = self.rect.move(pos[0] - self.x, 0)
        self.x = pos[0]
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.width - 150:
            self.rect.x = self.width - 150


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("gameover.png")
        self.rect = self.image.get_rect()
        self.rect.x = -950

    def update(self):
        if self.rect.x < 0:
            self.rect.x += 5


class Heart(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("heart.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

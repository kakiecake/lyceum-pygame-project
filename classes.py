import pygame
import random
from framework import event_handler
from load_image import load_image
from framework import Scene


class Board(Scene):
    def __init__(self, size, switch_to_menu):
        width, height = size
        self.width = width
        self.height = height
        self.switch_to_menu = switch_to_menu

    def update(self):
        if self.end_game is False:
            pygame.mouse.set_visible(False)
            self.ball.update()
            for brick in self.bricks:
                self.bricks_group.remove(brick)
                brick.update()
                if pygame.sprite.spritecollideany(brick, self.bricks_group) or \
                        pygame.sprite.spritecollideany(brick, self.vertical_barriers):
                    brick.on_brick_collision()
                self.bricks_group.add(brick)
            if pygame.sprite.spritecollideany(self.ball, self.dead_barriers):
                self.ball.die()
                for heart in self.hearts_group:
                    heart.kill()
                    break
                if self.life < 1:
                    self.life = -1
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
                    for i in range(len(self.bricks)):
                        if self.bricks[i] == brick:
                            del self.bricks[i]
                            break
                    pygame.sprite.spritecollide(self.ball, self.bricks_group, True)
                    self.ball.on_brick_collision(brick)
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
        if self.end_score is not None:
            self.end_score.render(screen)

    @event_handler(pygame.MOUSEMOTION, use_event=True)
    def on_move_mouse(self, event):
        self.platform.move(event.pos)

    @event_handler(pygame.KEYDOWN)
    def press_any_key_to_leave(self):
        if self.end_score is not None:
            pygame.mouse.set_visible(True)
            self.scene_data.update({"score": self.score})
            self.switch_to_menu()

    def end(self):
        self.end_game = True
        self.score += (1000 * (self.life + 1))
        self.score += ((self.number_of_bricks - len(self.bricks_group.sprites())) * 100)
        self.end_score = Score(self.score)

    def show(self):
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
        self.horizontal_barriers.add(Barrier(0, 0, self.width, 0))
        self.dead_barriers.add(Barrier(0, self.height - 20, self.width, self.height - 20))
        self.vertical_barriers.add(Barrier(0, 0, 0, self.height))
        self.vertical_barriers.add(Barrier(self.width, 0, self.width, self.height))
        self.ball = Ball((random.randint(0, 930), 450))
        self.balls_group.add(self.ball)
        self.platform = Platform((400, 470), self.width, index=self.scene_data.get('platform_index', 0))
        self.platforms_group.add(self.platform)
        self.bricks = [Brick((5 + 105 * i, 5 + 35 * j), index=self.scene_data.get('brick_index', 0)) for i in range(9)
                       for j in range(1)]
        self.bricks.append(Brick((320, 40), moving=True, index=self.scene_data.get('brick_index', 0)))
        self.bricks.append(Brick((5, 40), moving=True, index=self.scene_data.get('brick_index', 0)))
        self.bricks_group.add(*self.bricks)
        self.number_of_bricks = len(self.bricks_group.sprites())
        self.life = 2
        self.end_game = False
        self.score = 0
        self.end_score = None


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
    def __init__(self, pos, moving=False, index=0):
        super().__init__()
        if moving is True:
            self.image = load_image('brick_moving' + str(index) + '.png')
        else:
            self.image = load_image('brick' + str(index) + '.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vx = 1
        self.moving = moving

    def update(self):
        if self.moving is True:
            self.rect = self.rect.move(self.vx, 0)

    def on_brick_collision(self):
        if self.moving is True:
            if self.vx == 1:
                self.vx = -1
            else:
                self.vx = 1


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, width, index=0):
        super().__init__()
        self.image = load_image("platform" + str(index) + ".png")
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


class Score(pygame.sprite.Sprite):
    def __init__(self, score):
        super().__init__()
        self.rect = pygame.Rect(450, 225, 50, 50)
        self.font_color = (255, 255, 255)
        self.text = str(score)
        self.font = pygame.font.Font(None, 30)

    def render(self, screen):
        text = self.font.render(self.text, True, self.font_color)
        middle_x = self.rect.x + self.rect.width // 2
        middle_y = self.rect.y + self.rect.height // 2
        position = (middle_x - text.get_width() // 2,
                    middle_y - text.get_height() // 2)
        screen.blit(text, position)

import pygame
import random
from framework import event_handler
from load_image import load_image
from framework import Scene


class Board(Scene):
    def __init__(self, size, switch_to_menu, leaderboard_storage):
        width, height = size
        self.width = width
        self.height = height
        self.switch_to_menu = switch_to_menu
        self.leaderboard_storage = leaderboard_storage

    def create_new_ball(self):
        self.ball = Ball((random.randint(0, 930), 450),
                         self.scene_data["difficulty"])
        self.balls_group.add(self.ball)

    def update(self):
        if self.end_game:
            self.gameover.sprite.update()
        else:
            pygame.mouse.set_visible(False)

            self.ball.update()

            for brick in self.bricks_group:
                brick.update()
                collided_bricks = pygame.sprite.spritecollide(
                    brick, self.bricks_group, False)
                if len(collided_bricks) > 1 or \
                        pygame.sprite.spritecollideany(brick,
                                                       self.vertical_barriers):
                    brick.on_brick_collision()

            if pygame.sprite.spritecollideany(self.ball, self.dead_barriers):
                self.ball.die()
                self.hearts_group.sprites()[0].kill()
                if self.life < 1:
                    self.life = -1
                    self.end()
                else:
                    self.life -= 1
                    self.create_new_ball()

            if len(self.bricks_group.sprites()) == 0:
                self.end()

            if pygame.sprite.spritecollideany(self.ball,
                                              self.horizontal_barrier):
                self.ball.on_horizontal_collision()
            if pygame.sprite.spritecollideany(self.ball,
                                              self.vertical_barriers):
                self.ball.on_vertical_collision()

            for brick in self.bricks_group:
                if pygame.sprite.collide_rect(brick, self.ball):
                    if brick.life == 1:
                        brick.life = 0
                        brick.breaking()
                    else:
                        brick.kill()
                    self.ball.on_brick_collision(brick)

            if pygame.sprite.spritecollideany(self.platform.sprite,
                                              self.balls_group):
                self.ball.on_brick_collision(self.platform.sprite)

    def render(self, screen):
        self.balls_group.draw(screen)
        self.bricks_group.draw(screen)
        self.platform.draw(screen)
        self.gameover.draw(screen)
        self.hearts_group.draw(screen)
        if self.end_score is not None:
            self.end_score.render(screen)

    @event_handler(pygame.MOUSEMOTION, use_event=True)
    def on_move_mouse(self, event):
        self.platform.sprite.move(event.pos)

    @event_handler(pygame.KEYDOWN)
    def press_any_key_to_leave(self):
        if self.end_score is not None:
            pygame.mouse.set_visible(True)
            username = self.scene_data.get('username')
            if username:
                self.leaderboard_storage.add_new_score(username,
                                                       self.score, 'default')
            self.switch_to_menu()

    def end(self):
        self.end_game = True
        self.score += (1000 * (self.life + 1))
        self.score += ((self.number_of_bricks -
                        len(self.bricks_group.sprites())) * 100)
        self.end_score = Score(self.score)

    def show(self):
        self.platform = pygame.sprite.GroupSingle(
            Platform((400, 470), self.width,
                     index=self.scene_data.get('platform_index', 0)))
        self.balls_group = pygame.sprite.Group()
        self.bricks_group = pygame.sprite.Group()
        self.dead_barriers = pygame.sprite.Group()
        self.hearts_group = pygame.sprite.Group(
            Heart((55, 5)), Heart((30, 5)), Heart((5, 5)))
        self.gameover = pygame.sprite.GroupSingle(GameOver())
        self.dead_barriers.add(
            Barrier(0, self.height - 15, self.width, self.height - 15))

        self.vertical_barriers = pygame.sprite.Group(
            Barrier(0, 0, 0, self.height),
            Barrier(self.width, 0, self.width, self.height))

        self.horizontal_barrier = pygame.sprite.GroupSingle(
            Barrier(0, 0, self.width, 0))

        self.create_new_ball()

        default_brick_positions = [(5 + 105 * i, 5 + 35 * j, False)
                                   for i in range(9)
                                   for j in range(2)]
        brick_positions = self.scene_data.get(
            "bricks", default_brick_positions)

        self.make_bricks(brick_positions)

        self.number_of_bricks = len(self.bricks_group.sprites())
        self.life = 2
        self.end_game = False
        self.score = 0
        self.end_score = None

    def make_bricks(self, bricks):
        for brick_position in bricks:
            self.bricks_group.add(
                Brick(*brick_position,
                      sprite_index=self.scene_data.get('brick_index', 0)))


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos, difficulty):
        super().__init__()
        self.image = load_image("ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vx = random.choice((difficulty, -difficulty))
        self.vy = difficulty

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
            self.vx += random.randint(-4, 4)
        elif y > x:
            self.vx = -self.vx

    def on_vertical_collision(self):
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 950:
            self.rect.x = 930
        self.vx = -self.vx

    def on_horizontal_collision(self):
        self.vy = -self.vy

    def die(self):
        self.kill()


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, moving, sprite_index=0):
        super().__init__()
        if moving is True:
            self.image = load_image(
                f'brick_moving{str(sprite_index)}.png')
        else:
            self.image = load_image(f'brick{str(sprite_index)}.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 1
        self.moving = moving
        self.index = sprite_index
        self.life = 1

    def update(self):
        if self.moving is True:
            self.rect = self.rect.move(self.vx, 0)

    def on_brick_collision(self):
        if self.moving is True:
            if self.vx == 1:
                self.vx = -1
            else:
                self.vx = 1

    def breaking(self):
        if self.moving is True:
            self.image = load_image(
                f'broken_brick_moving{str(self.index)}.png')
        else:
            self.image = load_image(f'broken_brick{str(self.index)}.png')


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

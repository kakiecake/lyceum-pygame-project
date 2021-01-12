import pygame
from framework import event_handler, Scene
from load_image import load_image


class Customization(Scene):
    def __init__(self, switch_to_menu=lambda data: None):
        self.bricks_group = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.stars_group = pygame.sprite.Group()
        self.button = Button()
        self.bricks_group.add(*[Brick((25 + 187 * i, 25), number=i) for i in range(4)])
        self.bricks_group.add(*[Brick((25 + 187 * i, 55), moving=True, number=i) for i in range(4)])
        self.platforms_group.add(*[Platform((25 + 374 * i, 250), number=i) for i in range(2)])
        self.star1 = Star((130, 25))
        self.star2 = Star((180, 229))
        self.stars_group.add(self.star1, self.star2)
        self.bricks = [[(25, 25), (25, 55)], [(212, 25), (212, 55)], [(399, 25), (399, 55)], [(586, 25), (586, 55)]]
        self.platforms = [(25, 250), (399, 250)]
        self.brick = 0
        self.platform = 0
        self.switch_to_menu = switch_to_menu

    def update(self):
        pass

    def render(self, screen):
        self.bricks_group.draw(screen)
        self.platforms_group.draw(screen)
        self.stars_group.draw(screen)
        self.button.render(screen)

    @event_handler(pygame.MOUSEBUTTONDOWN, use_event=True)
    def mouse_click(self, event):
        leave = False
        for brick in self.bricks_group:
            if brick.rect.collidepoint(event.pos):
                for i in range(len(self.bricks)):
                    for j in self.bricks[i]:
                        if brick.rect.x == j[0] and brick.rect.y == j[1]:
                            self.brick = i
                            self.star1.rect.x = brick.rect.x + 105
                            leave = True
                            break
                    if leave is True:
                        break
            if leave is True:
                break
        leave = False
        for platform in self.platforms_group:
            if platform.rect.collidepoint(event.pos):
                for i in range(len(self.platforms)):
                    if platform.rect.x == self.platforms[i][0] and platform.rect.y == self.platforms[i][1]:
                        self.platform = i
                        self.star2.rect.x = platform.rect.x + 155
                        leave = True
                        break
                if leave is True:
                    break
        if self.button.rect.collidepoint(event.pos):
            self.save()

    def save(self):
        self.scene_data.update({"brick_index": self.brick, "platform_index": self.platform})
        self.switch_to_menu()


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos, moving=False, number=0):
        super().__init__()
        if moving is True:
            self.image = load_image(f"brick_moving{number}.png")
        else:
            self.image = load_image(f"brick{number}.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, number=0):
        super().__init__()
        self.image = load_image(f"platform{number}.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Star(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("star.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(400, 450, 150, 50)
        self.color = (255, 0, 0)
        self.font_color = (255, 255, 255)
        self.text = 'Сохранить'
        self.font = pygame.font.Font(None, 42)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, True, self.font_color)
        middle_x = self.rect.x + self.rect.width // 2
        middle_y = self.rect.y + self.rect.height // 2
        position = (middle_x - text.get_width() // 2,
                    middle_y - text.get_height() // 2)
        screen.blit(text, position)

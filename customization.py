import pygame
from framework import event_handler, Scene, Button
from load_image import load_image


class Customization(Scene):
    def __init__(self, switch_to_menu=lambda data: None):
        self.bricks_group = pygame.sprite.Group()
        self.bricks_group.add(
            *[Brick((25 + 187 * i, 25), number=i) for i in range(4)])
        self.bricks_group.add(
            *[Brick((25 + 187 * i, 55), moving=True, number=i)
              for i in range(4)])

        self.platforms_group = pygame.sprite.Group(
            *[Platform((25 + 374 * i, 250), number=i) for i in range(2)])

        self.button = Button(pygame.Rect(400, 450, 150, 50),
                             self.save, text='Сохранить')

        self.brick_star = Star((130, 25))
        self.platform_star = Star((180, 229))
        self.stars_group = pygame.sprite.Group(
            self.brick_star, self.platform_star)

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
        # Проверка на нажатие кнопки сохранения
        self.button.handle_click(event)
        # Проверяем было ли нажатие по кирпичам
        for i, brick in enumerate(self.bricks_group):
            # Если было, то выбираем соответствующий набор спрайтов
            if brick.rect.collidepoint(event.pos):
                self.brick_star.rect.x = brick.rect.x + 105
                self.brick = i // 2
        # Проверяем на нажатие по платформам
        for i, platform in enumerate(self.platforms_group):
            # Если было, то выбираем соответствующую платформу
            if platform.rect.collidepoint(event.pos):
                self.platform_star.rect.x = platform.rect.x + 155
                self.platform = i // 2

    def save(self):
        # Сохраняем информацию о выбраных спрайтах
        self.scene_data.update(
            {"brick_index": self.brick, "platform_index": self.platform})
        # Выходим в меню
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

import pygame
from framework import event_handler, Scene
from load_image import load_image


class Designer(Scene):
    def __init__(self, switch_to_menu):
        self.bricks_group = pygame.sprite.Group()
        self.bricks = []
        self.button = Button()
        self.switch_to_menu = switch_to_menu

    def update(self):
        pass

    def render(self, screen):
        self.bricks_group.draw(screen)
        self.button.render(screen)

    @event_handler(pygame.MOUSEBUTTONDOWN, button=1, use_event=True)
    def left_mouse_button_click(self, event):
        brick = Brick(event.pos)
        if not(pygame.sprite.spritecollideany(brick, self.bricks_group)) and event.pos[0] < 850 and \
                event.pos[1] < 470:
            self.bricks.append(event.pos)
            self.bricks_group.add(brick)
        elif self.button.rect.collidepoint(event.pos):
            self.save()

    @event_handler(pygame.MOUSEBUTTONDOWN, button=2, use_event=True)
    def middle_mouse_button_click(self, event):
        brick = Brick(event.pos, moving=True)
        if not(pygame.sprite.spritecollideany(brick, self.bricks_group)) and event.pos[0] < 850 and \
                event.pos[1] < 470:
            self.bricks.append([event.pos, True])
            self.bricks_group.add(brick)

    @event_handler(pygame.MOUSEBUTTONDOWN, button=3, use_event=True)
    def right_mouse_button_click(self, event):
        for brick in self.bricks_group:
            if brick.rect.collidepoint(event.pos):
                brick.kill()

    def save(self):
        self.scene_data.update({"bricks": self.bricks})
        self.switch_to_menu()


class Brick(pygame.sprite.Sprite):
    def __init__(self, pos, moving=False):
        super().__init__()
        if moving is True:
            self.image = load_image("brick_moving0.png")
        else:
            self.image = load_image("brick0.png")
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(800, 470, 150, 30)
        self.color = (255, 0, 0)
        self.font_color = (255, 255, 255)
        self.text = 'Сохранить'
        self.font = pygame.font.Font(None, 30)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, True, self.font_color)
        middle_x = self.rect.x + self.rect.width // 2
        middle_y = self.rect.y + self.rect.height // 2
        position = (middle_x - text.get_width() // 2,
                    middle_y - text.get_height() // 2)
        screen.blit(text, position)

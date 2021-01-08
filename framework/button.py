from typing import Callable
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, on_click: Callable,
                 color=(255, 0, 0), font_color=(255, 255, 255),
                 text="", font=None):
        super().__init__()
        self.rect = rect
        self.on_click = on_click
        self.color = color
        self.font_color = font_color
        self.text = text
        self.font = font or pygame.font.Font(None, 36)

    def handle_click(self, clicked_event):
        pos = clicked_event.pos
        if self.rect.collidepoint(pos):
            self.on_click()

    def update(self):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = self.font.render(self.text, True, self.font_color)
        middle_x = self.rect.x + self.rect.width // 2
        middle_y = self.rect.y + self.rect.height // 2
        position = (middle_x - text.get_width() // 2,
                    middle_y - text.get_height() // 2)
        screen.blit(text, position)

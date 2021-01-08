import pygame
from pygame import Rect
from framework import Button, loop, event_handler


class Menu:
    def __init__(self, go_to_level=lambda: None, go_to_leaderboard=lambda: None):
        self.buttons = pygame.sprite.Group()
        self.start_button = Button(
            Rect(400, 300, 200, 100), go_to_level, text="Старт")
        self.leaderboard_button = Button(
            Rect(400, 600, 200, 100), go_to_leaderboard, text="Лидеры")
        self.buttons.add(self.start_button)
        self.buttons.add(self.leaderboard_button)

    @event_handler(pygame.MOUSEBUTTONDOWN, use_event=True)
    def handle_click(self, event):
        self.start_button.handle_click(event)
        self.leaderboard_button.handle_click(event)

    def update(self):
        pass

    def render(self, screen):
        for button in self.buttons:
            button.render(screen)


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    menu = Menu()
    size = (1000, 1000)
    screen = pygame.display.set_mode(size)
    loop([menu], screen)

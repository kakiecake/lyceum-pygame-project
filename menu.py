import pygame
from pygame import Rect
from framework import Button, loop, event_handler, Scene


class Menu(Scene):
    def __init__(self,
                 go_to_level=lambda: None,
                 go_to_leaderboard=lambda: None,
                 go_to_registration=lambda: None,
                 go_to_designer=lambda: None):

        self.start_button = Button(
            Rect(50, 200, 250, 100), go_to_level, text="Старт")
        self.leaderboard_button = Button(
            Rect(350, 200, 250, 100), go_to_leaderboard, text="Лидеры")
        self.registration_button = Button(
            Rect(650, 200, 250, 100), go_to_registration, text="Вход/Регистрация")
        self.designer_button = Button(
            Rect(350, 400, 250, 100), go_to_designer, text="Конструктор уровней")

    @event_handler(pygame.MOUSEBUTTONDOWN, use_event=True)
    def handle_click(self, event):
        self.start_button.handle_click(event)
        self.leaderboard_button.handle_click(event)
        self.registration_button.handle_click(event)
        self.designer_button.handle_click(event)

    def update(self):
        pass

    def render(self, screen):
        self.registration_button.render(screen)
        self.leaderboard_button.render(screen)
        self.start_button.render(screen)
        self.designer_button.render(screen)

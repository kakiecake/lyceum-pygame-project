import pygame
from pygame import Rect
from framework import Button, loop, event_handler, Scene


class Menu(Scene):
    def __init__(self,
                 go_to_level=lambda: None,
                 go_to_leaderboard=lambda: None,
                 go_to_registration=lambda: None,
                 go_to_designer=lambda: None,
                 go_to_customization=lambda: None):

        self.start_button = Button(
            Rect(50, 120, 250, 100), go_to_level, text="Старт")
        self.leaderboard_button = Button(
            Rect(350, 120, 250, 100), go_to_leaderboard, text="Лидеры")
        self.registration_button = Button(
            Rect(650, 120, 250, 100), go_to_registration, text="Вход/Регистрация")
        self.designer_button = Button(
            Rect(180, 300, 280, 100), go_to_designer, text="Конструктор уровней")
        self.customization_button = Button(
            Rect(530, 300, 250, 100), go_to_customization, text="Кастомизация")

    @event_handler(pygame.MOUSEBUTTONDOWN, use_event=True)
    def handle_click(self, event):
        self.start_button.handle_click(event)
        self.leaderboard_button.handle_click(event)
        self.registration_button.handle_click(event)
        self.designer_button.handle_click(event)
        self.customization_button.handle_click(event)

    def update(self):
        pass

    def render(self, screen):
        self.registration_button.render(screen)
        self.leaderboard_button.render(screen)
        self.start_button.render(screen)
        self.designer_button.render(screen)
        self.customization_button.render(screen)

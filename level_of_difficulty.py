import pygame
from framework import event_handler, Scene, Button


class Difficulty(Scene):
    def __init__(self, switch_to_menu=lambda data: None):
        self.hard = Button(pygame.Rect(650, 200, 250, 100), lambda: self.start(-10), text='Сложный')
        self.medium = Button(pygame.Rect(350, 200, 250, 100), lambda: self.start(-6), text='Средний')
        self.easy = Button(pygame.Rect(50, 200, 250, 100), lambda: self.start(-3), text='Лёгкий')
        self.switch_to_menu = switch_to_menu

    def update(self):
        pass

    def render(self, screen):
        self.hard.render(screen)
        self.medium.render(screen)
        self.easy.render(screen)

    @event_handler(pygame.MOUSEBUTTONDOWN, use_event=True)
    def mouse_click(self, event):
        self.hard.handle_click(event)
        self.medium.handle_click(event)
        self.easy.handle_click(event)

    def start(self, difficulty):
        self.scene_data.update({"difficulty": difficulty})
        self.switch_to_menu()

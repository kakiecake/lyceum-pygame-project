import pygame
from framework import Scene


class Leaderboard(Scene):
    def __init__(self):
        self.font = pygame.font.Font(None, 40)

    def update(self):
        pass

    def render(self, screen):
        username = self.scene_data.get('username', 'гость')
        text = self.font.render(
            f'Таблица лидеров. Пользователь: {username}', True, (0, 0, 0))
        text_width, text_height = text.get_size()
        screen_width, screen_height = screen.get_size()
        position = (screen_width // 2 - text_width // 2,
                    screen_height // 2 - text_height // 2)
        screen.blit(text, position)

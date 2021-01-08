import pygame


class Leaderboard:
    def __init__(self):
        self.text = pygame.font.Font(None, 40).render(
            'Таблица лидеров', True, (0, 0, 0))

    def update(self):
        pass

    def render(self, screen):
        text_width, text_height = self.text.get_size()
        screen_width, screen_height = screen.get_size()
        position = (screen_width // 2 - text_width // 2,
                    screen_height // 2 - text_height // 2)
        screen.blit(self.text, position)

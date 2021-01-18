import pygame
from framework import Scene, Button, event_handler
from leaderboard_storage import LeaderboardStorage


class Leaderboard(Scene):
    def __init__(self, leaderboard_storage: LeaderboardStorage):
        self.font = pygame.font.Font(None, 40)
        self.storage = leaderboard_storage
        self.level = 'default'
        self.should_view_all = True
        self.switch_view_button = Button(
            pygame.Rect(650, 400, 280, 70),
            text='Поменять отображение',
            on_click=self.switch_view)
        self.get_scores()

    @event_handler(pygame.MOUSEBUTTONDOWN, use_event=True)
    def handle_click(self, event):
        self.switch_view_button.handle_click(event)

    def switch_view(self):
        self.should_view_all = not self.should_view_all
        self.get_scores()

    def get_scores(self):
        self.scores = self.storage.get_all_level_scores(
            self.level) if self.should_view_all else \
            self.storage.get_unique_level_scores(self.level)

    def update(self):
        pass

    def render(self, screen):
        TEXT_START = 100

        title = self.font.render(self.level, (0, 0, 0), True)
        position = (
            screen.get_width() // 2 - title.get_width() // 2,
            20)
        screen.blit(title, position)

        for i, score in enumerate(self.scores):
            text = f'{score.user.ljust(40)}{score.score}'
            rendered_text = self.font.render(text, (0, 0, 0), True)
            position = (200, TEXT_START + i * rendered_text.get_height())
            screen.blit(rendered_text, position)

        self.switch_view_button.render(screen)

    def show(self):
        self.get_scores()

import pygame


class TextEdit:
    def __init__(self, rect: pygame.Rect, on_submit=lambda text: None, text="", color=(0, 0, 0), padding=5):
        self.rect = rect
        self.active = False
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        self.padding = padding

    def handle_click(self, clicked_event):
        if self.rect.collidepoint(clicked_event.pos):
            self.active = True
        else:
            self.active = False

    def handle_keydown(self, keydown_event):
        if not self.active:
            return
        if keydown_event.key == pygame.K_ESCAPE:
            self.active = False
        elif keydown_event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        self.text += keydown_event.unicode

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, width=2)

        text = self.font.render(self.text, True, self.color)
        text_width, text_height = text.get_size()
        x_offset = text_width - self.rect.width if text_width > self.rect.width else 0
        position = (self.rect.x + self.padding - x_offset,
                    self.rect.y + self.rect.height // 2 - text_height // 2)
        screen.set_clip(self.rect)
        screen.blit(text, position)
        screen.set_clip(None)

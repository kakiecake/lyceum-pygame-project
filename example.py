import pygame
from framework import event_handler, main


class Ball:
    """Тестовый класс для использования обработчиков событий"""
    color_active = (255, 100, 100)
    color_inactive = (150, 150, 250)

    def __init__(self):
        self.is_active = False

    # для установки обработчика событий используется декоратор
    # в качестве аргументов можно указать события с какими свойствами нам нужны
    # в данном примере эта функция вызывается каждый раз, когда появляется событие
    # pygame.KEYDOWN с полем key равным K_SPACE, то есть при каждом нажатии на пробел
    @event_handler(pygame.KEYDOWN, key=pygame.K_SPACE)
    def change_active(self):
        self.is_active = not self.is_active

    # если необходим доступ к сырому объекту события,
    # нужно указать параметр use_event=True
    # в таком случае событие будет передано каждый раз при вызове этой функции
    @event_handler(pygame.MOUSEBUTTONDOWN, use_event=True)
    def mouse_clicked(self, event):
        print('Клик', event.pos)

    def render(self, screen):
        color = self.color_active if self.is_active \
            else self.color_inactive
        pygame.draw.circle(screen, color, (100, 100), 50)


if __name__ == "__main__":
    ball = Ball()
    main([ball])

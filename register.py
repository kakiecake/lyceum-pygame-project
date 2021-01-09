from framework import TextEdit, Button, event_handler
from pygame import Rect, KEYDOWN, MOUSEBUTTONDOWN
from user_storage import UserStorage
import pygame


class RegisterScene:
    font_color = (0, 0, 0)

    def __init__(self, user_storage: UserStorage):
        self.font = pygame.font.Font(None, 24)
        self.user_storage = user_storage
        self.login_edit = TextEdit(Rect(100, 100, 200, 50))
        self.password_edit = TextEdit(Rect(100, 170, 200, 50))
        self.login_button = Button(
            Rect(100, 250, 200, 40),
            on_click=self.on_login_button_click,
            text="Логин")
        self.register_button = Button(
            Rect(100, 300, 200, 40),
            on_click=self.on_register_button_click,
            text="Регистрация")
        self.error_message = ""

    @event_handler(KEYDOWN, use_event=True)
    def on_keydown(self, event):
        self.login_edit.handle_keydown(event)
        self.password_edit.handle_keydown(event)

    @event_handler(MOUSEBUTTONDOWN, use_event=True)
    def on_click(self, event):
        self.login_edit.handle_click(event)
        self.password_edit.handle_click(event)
        self.register_button.handle_click(event)
        self.login_button.handle_click(event)

    def validate_login(self, login: str) -> bool:
        if login == '':
            self.error_message = "Логин не может быть пустым"
            return False
        if not 6 <= len(login) <= 30:
            self.error_message = "Логин должен иметь длину от 6 до 30 символов"
            return False
        return True

    def validate_password(self, password: str) -> bool:
        if password == '':
            self.error_message = "Пароль не может быть пустым"
            return False
        if not 6 <= len(password) <= 30:
            self.error_message = "Пароль должен иметь длину от 6 до 30 символов"
            return False
        return True

    def on_login_button_click(self):
        login = self.login_edit.text
        password = self.password_edit.text
        success = self.user_storage.login_user(login, password)
        self.error_message = "Пользователь успешно вошел" \
            if success else "Комбинация логин/пароль неверна"

    def on_register_button_click(self):
        login = self.login_edit.text
        password = self.password_edit.text
        if not self.validate_login(login) or not self.validate_password(password):
            return
        success = self.user_storage.register_user(login, password)
        self.error_message = "Регистрация прошла успешно" \
            if success else "Ошибка регистрации"

    def update(self):
        pass

    def render(self, screen):
        self.login_edit.render(screen)
        self.password_edit.render(screen)
        self.login_button.render(screen)
        self.register_button.render(screen)

        text = self.font.render(self.error_message, True, self.font_color)
        screen.blit(text, (60, 50))

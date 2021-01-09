from menu import Menu
from leaderboard import Leaderboard
from framework import SceneManager, loop
from classes import Board
from register import RegisterScene
from user_storage import UserStorage
import pygame
import sqlite3
from pathlib import Path

DATABASE_PATH = Path('./db.sqlite')

if __name__ == '__main__':
    connection = sqlite3.connect(DATABASE_PATH)
    user_storage = UserStorage(connection)

    pygame.init()
    pygame.font.init()
    size = (950, 500)

    scene_manager = SceneManager()
    menu = Menu(go_to_leaderboard=lambda: scene_manager.switch_to('leaderboard'),
                go_to_level=lambda: scene_manager.switch_to('board'),
                go_to_registration=lambda: scene_manager.switch_to('registration'))
    leaderboard = Leaderboard()
    board = Board(size)
    register_scene = RegisterScene(user_storage)

    scene_manager.add_scene('board', board)
    scene_manager.add_scene('menu', menu)
    scene_manager.add_scene('leaderboard', leaderboard)
    scene_manager.add_scene('registration', register_scene)
    scene_manager.switch_to('menu')

    screen = pygame.display.set_mode(size)
    loop(scene_manager, screen)

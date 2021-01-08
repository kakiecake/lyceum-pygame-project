from menu import Menu
from leaderboard import Leaderboard
from framework import SceneManager, loop
from classes import Board
import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    size = (950, 500)

    scene_manager = SceneManager()
    menu = Menu(go_to_leaderboard=lambda: scene_manager.switch_to('leaderboard'),
                go_to_level=lambda: scene_manager.switch_to('board'))
    leaderboard = Leaderboard()
    board = Board(size)

    scene_manager.add_scene('board', board)
    scene_manager.add_scene('menu', menu)
    scene_manager.add_scene('leaderboard', leaderboard)
    scene_manager.switch_to('menu')

    screen = pygame.display.set_mode(size)
    loop(scene_manager, screen)

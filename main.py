from menu import Menu
from leaderboard import Leaderboard
from framework import SceneManager, loop
import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    scene_manager = SceneManager()
    menu = Menu(go_to_leaderboard=lambda: scene_manager.switch_to('leaderboard'))
    leaderboard = Leaderboard()

    scene_manager.add_scene('menu', menu)
    scene_manager.add_scene('leaderboard', leaderboard)
    scene_manager.switch_to('menu')

    size = (1000, 1000)
    screen = pygame.display.set_mode(size)
    loop(scene_manager, screen)

import pygame
import sys
import os


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print("Файл не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

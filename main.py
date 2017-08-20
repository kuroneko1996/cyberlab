import pygame
from menu import main_menu


def main():
    pygame.init()
    pygame.joystick.init()
    main_menu().run()


if __name__ == '__main__':
    main()

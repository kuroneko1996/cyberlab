import pygame as pg
from settings import *
from nanogui import Nanogui
from .game_screen import GameScreen


class SettingsScreen(GameScreen):
    def __init__(self, display):
        super().__init__(display)
        self.gui = Nanogui(display)

    def update(self):
        self.gui.pre(self.joystick)

        if self.gui.button('btn_back', 'Back', 240, 128, 64, 32):
            return True

        self.gui.after()

    def draw(self):
        #if self.updated:
        self.display.fill(BG_COLOR)

        self.draw_game_title()
        self.gui.draw()

        pg.display.flip()

    def draw_game_title(self):
        surface = self.font.render(GAME_TITLE, True, (255, 255, 255))
        x = SCREEN_WIDTH // 2 - surface.get_width() // 2
        y = 40
        self.display.blit(surface, (x, y))

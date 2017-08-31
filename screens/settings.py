import pygame as pg
from settings import *
from nanogui import Nanogui
from .game_screen import GameScreen


class SettingsScreen(GameScreen):
    def __init__(self, display):
        super().__init__(display)
        self.gui = Nanogui(display)

        self.music_volume = 100.0
        self.sfx_volume = 100.0
        self.master_volume = 100.0

    def update(self):
        self.gui.pre(self.joystick)

        # Master Volume Slider
        (changed, self.master_volume) = self.gui.slider(
            'master_volume', self.master_volume, 0, 100, SCREEN_WIDTH // 2 - 64, 140, 128)
        if changed:
            print("New Master Volume {}".format(self.master_volume))

        # Music Volume Slider
        (changed, self.music_volume) = self.gui.slider(
            'music_volume', self.music_volume, 0, 100, SCREEN_WIDTH // 2 - 64, 220, 128)
        if changed:
            print("New Music Volume {}".format(self.music_volume))

        # SFX Volume Slider
        (changed, self.sfx_volume) = self.gui.slider(
            'sfx_volume', self.sfx_volume, 0, 100, SCREEN_WIDTH // 2 - 64, 300, 128)
        if changed:
            print("New Sound Volume {}".format(self.sfx_volume))

        if self.gui.button('btn_save', 'Save', SCREEN_WIDTH // 2 - 64, 360, 128, 32):
            print("Options Saved")

        if self.gui.button('btn_back', 'Back', SCREEN_WIDTH // 2 + 64 + 16, 360, 64, 32):
            return True

        self.gui.after()

    def draw(self):
        #if self.updated:
        self.display.fill(BG_COLOR)

        self.draw_game_title()

        self.draw_text_centered(SCREEN_WIDTH // 2, 100, 'Master Volume', (128, 135, 239))
        self.draw_text_centered(SCREEN_WIDTH // 2, 180, 'Music Volume', (128, 135, 239))
        self.draw_text_centered(SCREEN_WIDTH // 2, 260, 'Sfx Volume', (128, 135, 239))
        self.gui.draw()

        pg.display.flip()

    def draw_game_title(self):
        surface = self.font.render(GAME_TITLE, True, (255, 255, 255))
        x = SCREEN_WIDTH // 2 - surface.get_width() // 2
        y = 40
        self.display.blit(surface, (x, y))

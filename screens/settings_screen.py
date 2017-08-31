import pygame as pg
import configparser
import settings
from nanogui import Nanogui
from .game_screen import GameScreen


class SettingsScreen(GameScreen):
    def __init__(self, display):
        super().__init__(display)
        self.gui = Nanogui(display)

        self.master_volume = settings.MASTER_VOLUME
        self.music_volume = settings.MUSIC_VOLUME
        self.sfx_volume = settings.SFX_VOLUME

    def update(self):
        self.gui.pre(self.joystick, self.mousedown)

        # Master Volume Slider
        (changed, self.master_volume) = self.gui.slider(
            'master_volume', self.master_volume, 0, 100, settings.SCREEN_WIDTH // 2 - 64, 140, 128)
        if changed:
            print("New Master Volume {}".format(self.master_volume))

        # Music Volume Slider
        (changed, self.music_volume) = self.gui.slider(
            'music_volume', self.music_volume, 0, 100, settings.SCREEN_WIDTH // 2 - 64, 220, 128)
        if changed:
            print("New Music Volume {}".format(self.music_volume))

        # SFX Volume Slider
        (changed, self.sfx_volume) = self.gui.slider(
            'sfx_volume', self.sfx_volume, 0, 100, settings.SCREEN_WIDTH // 2 - 64, 300, 128)
        if changed:
            print("New Sound Volume {}".format(self.sfx_volume))

        if self.gui.button('btn_save', 'Save', settings.SCREEN_WIDTH // 2 - 64, 360, 128, 32):
            print("Options Saved")
            self.save_to_file()

        if self.gui.button('btn_back', 'Back', settings.SCREEN_WIDTH // 2 + 64 + 16, 360, 64, 32):
            return True

        self.gui.after()

    def draw(self):
        #if self.updated:
        self.display.fill(settings.BG_COLOR)

        self.draw_game_title()

        self.draw_text_centered(settings.SCREEN_WIDTH // 2, 100, 'Master Volume', (128, 135, 239))
        self.draw_text_centered(settings.SCREEN_WIDTH // 2, 180, 'Music Volume', (128, 135, 239))
        self.draw_text_centered(settings.SCREEN_WIDTH // 2, 260, 'Sfx Volume', (128, 135, 239))
        self.gui.draw()

        pg.display.flip()

    def draw_game_title(self):
        surface = self.font.render(settings.GAME_TITLE, True, (255, 255, 255))
        x = settings.SCREEN_WIDTH // 2 - surface.get_width() // 2
        y = 40
        self.display.blit(surface, (x, y))

    def save_to_file(self):
        filename = 'user_settings.cfg'
        config = configparser.ConfigParser()
        config.read(filename)

        settings.MASTER_VOLUME = self.master_volume
        settings.MUSIC_VOLUME = self.music_volume
        settings.SFX_VOLUME = self.sfx_volume

        config['SOUND']['MASTER_VOLUME'] = str(self.master_volume)
        config['SOUND']['MUSIC_VOLUME'] = str(self.music_volume)
        config['SOUND']['SFX_VOLUME'] = str(self.sfx_volume)

        with open(filename, 'w') as configfile:
            config.write(configfile)

import sys
import pygame as pg
from settings import *


class GameScreen:
    def __init__(self, display):
        self.clock = pg.time.Clock()
        self.dt = 0.0
        self.playing = True
        self.display = display
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)
        self.font = pg.font.Font(*FONT_BIGGER)

        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
        self.joystick = None
        if len(self.joysticks) > 0:
            self.joystick = self.joysticks[0]
            self.joystick.init()

        self.mousex = 0.0
        self.mousey = 0.0

        self.updated = True

    def run(self):
        self.draw()  # draw first time to ignore self.updated
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            if self.events():
                break
            if self.update():
                break
            self.draw()

    def events(self):
        self.updated = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()

    def update(self):
        pass

    def draw(self):
        pass

    def quit_game(self):
        pg.quit()
        sys.exit()

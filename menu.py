import time
import pygame as pg
import sys
from game import Game
from settings import *
from nanogui import Nanogui

OPTION_COLOR = (231, 100, 240)

SELECTED_OPTION_COLOR = (255, 100, 30)

INITIAL_V_GAP = 30

V_SPACING = 5


class Menu:
    def __init__(self, menu, display):
        self.clock = pg.time.Clock()
        self.dt = 0.0
        self.playing = True
        self.display = display
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)
        self.font = pg.font.SysFont("comicsansms", 72)

        self.updated = True

        self.menu = menu
        self.gui = Nanogui()

        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
        self.joystick = None
        if len(self.joysticks) > 0:
            self.joystick = self.joysticks[0]
            self.joystick.init()

        self.last_axis_motion = 0.0

    def run(self):
        self.draw()  # draw first time to ignore self.updated
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        self.updated = False
        action = None

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game(self)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_game(self)
                if event.key == pg.K_DOWN:
                    action = 'down'
                if event.key == pg.K_UP:
                    action = 'up'
                if event.key == pg.K_RETURN:
                    action = 'enter'
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == J_BUTTONS['A']:
                    action = 'enter'
            if event.type == pg.JOYAXISMOTION:
                if event.dict['axis'] == 1:
                    if time.time() >= self.last_axis_motion + 0.3:
                        if event.dict['value'] < -JOYSTICK_THRESHOLD:
                            action = 'up'
                            self.last_axis_motion = time.time()
                        elif event.dict['value'] > JOYSTICK_THRESHOLD:
                            action = 'down'
                            self.last_axis_motion = time.time()

        if action == 'down':
            self.menu["selected_option"] += 1
            self.menu["selected_option"] %= len(self.menu["options"])
            self.updated = True
        elif action == 'up':
            self.menu["selected_option"] -= 1
            self.menu["selected_option"] %= len(self.menu["options"])
            self.updated = True
        elif action == 'enter':
            self.menu["options"][self.menu["selected_option"]]["func"](self)

    def update(self):
        self.gui.pre(self.joystick)
        self.gui.after()

    def draw(self):
        if self.updated:
            self.display.fill(BG_COLOR)
            self.draw_options()
            pg.display.flip()

    def draw_options(self):
        count = 0

        for option in self.menu["options"]:
            if self.menu["selected_option"] == count:
                color = SELECTED_OPTION_COLOR
            else:
                color = OPTION_COLOR

            rend = self.font.render(option["name"], True, color)
            rect = rend.get_rect().move(
                SCREEN_WIDTH // 2 - rend.get_width() // 2,
                INITIAL_V_GAP + (rend.get_height() + V_SPACING) * count)

            self.display.blit(rend, rect)

            count += 1


def new_game(self):
    self.playing = False

    game = Game(self.display)
    game.load()
    game.run()


def quit_game(self):
    pg.quit()
    sys.exit()


def load_game(self):
    print("LOAD GAME")
    # TODO: finish load game option


def settings(self):
    print("SETTINGS")
    # TODO: finish settings option


def main_menu(display):
    return Menu({
        "selected_option": 0,
        "options": [
            {
                "name": "NEW GAME",
                "func": new_game
            },
            {
                "name": "LOAD GAME",
                "func": load_game
            },
            {
                "name": "SETTINGS",
                "func": settings
            },
            {
                "name": "QUIT",
                "func": quit_game
            },
        ]
    }, display)

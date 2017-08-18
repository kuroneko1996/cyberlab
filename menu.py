import pygame as pg
import sys
from game import Game
from settings import *

OPTION_COLOR = (231, 100, 240)

SELECTED_OPTION_COLOR = (255, 100, 30)

INITIAL_V_GAP = 30

V_SPACING = 5

display = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Menu:
    def __init__(self, menu, display):
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000
        self.playing = True
        self.display = display
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)

        self.menu = menu

    def run(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game(self)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_game(self)
                if event.key == pg.K_DOWN:
                    self.menu["selected_option"] += 1
                    self.menu["selected_option"] %= len(self.menu["options"])
                if event.key == pg.K_UP:
                    self.menu["selected_option"] -= 1
                    self.menu["selected_option"] %= len(self.menu["options"])
                if event.key == pg.K_RETURN:
                    self.menu["options"][self.menu["selected_option"]]["func"](self)

    def update(self):
        pass

    def draw(self):
        self.display.fill(BG_COLOR)

        count = 0

        for option in self.menu["options"]:
            font = pg.font.SysFont("comicsansms", 72)

            if self.menu["selected_option"] == count:
                color = SELECTED_OPTION_COLOR
            else:
                color = OPTION_COLOR

            rend = font.render(option["name"], True, color)
            rect = rend.get_rect().move(
                SCREEN_WIDTH // 2 - rend.get_width() // 2,
                INITIAL_V_GAP + (rend.get_height() + V_SPACING) * count)

            self.display.blit(rend, rect)

            count += 1

        pg.display.flip()


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


main_menu = Menu({
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

settings = Menu({
    "selected_option": 0,
    "options": [
        # TODO: finish
    ]
}, display)

pause = Menu({
    "selected_option": 0,
    "options": [
        # TODO: finish
    ]
}, display)

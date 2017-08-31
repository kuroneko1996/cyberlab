import time
import pygame as pg
import sys
from game import Game
from screens.settings_screen import SettingsScreen
from screens.game_screen import GameScreen
from settings import *

OPTION_COLOR = (128, 135, 239)

SELECTED_OPTION_COLOR = (255, 255, 255)

INITIAL_V_GAP = 140

V_SPACING = 5


class Menu(GameScreen):
    def __init__(self, menu, display):
        super().__init__(display)

        self.menu = menu
        self.menu_rects = {}

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
            # keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_game(self)
                if event.key == pg.K_DOWN:
                    action = 'down'
                if event.key == pg.K_UP:
                    action = 'up'
                if event.key == pg.K_RETURN:
                    action = 'enter'
            # mouse
            if event.type == pg.MOUSEMOTION:
                self.mousex, self.mousey = pg.mouse.get_pos()
                for i in range(len(self.menu_rects.items())):
                    if self.menu_rects[i].collidepoint(self.mousex, self.mousey):
                        self.menu['selected_option'] = i
                        self.updated = True
                        break
            if event.type == pg.MOUSEBUTTONDOWN:
                for i in range(len(self.menu_rects.items())):
                    if self.menu_rects[i].collidepoint(self.mousex, self.mousey):
                        action = 'enter'
                        break
            # joystick
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
        pass

    def draw(self):
        if self.updated:
            self.display.fill(BG_COLOR)
            self.draw_game_title()
            self.draw_options()
            pg.display.flip()

    def draw_options(self):
        count = 0
        x_offset = 0

        for option in self.menu["options"]:
            if self.menu["selected_option"] == count:
                color = SELECTED_OPTION_COLOR
            else:
                color = OPTION_COLOR

            rend = self.font.render(option["name"], True, color)
            if x_offset == 0:
                x_offset = SCREEN_WIDTH // 2 - rend.get_width() // 2

            rect = rend.get_rect().move(
                x_offset,
                INITIAL_V_GAP + (rend.get_height() + V_SPACING) * count)
            self.menu_rects[count] = rect

            self.display.blit(rend, rect)

            count += 1

    def draw_game_title(self):
        surface = self.font.render(GAME_TITLE, True, (255, 255, 255))
        x = SCREEN_WIDTH // 2 - surface.get_width() // 2
        y = 40
        self.display.blit(surface, (x, y))


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
    SettingsScreen(self.display).run()
    self.updated = True


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

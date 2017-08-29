from operator import add
from settings import *
from .sprite import Sprite
import pygame as pg
from triggers.triggers import KeyButtonTrigger

DOOR_THICKNESS = 8


def move(center, shift):
    return tuple(map(add, center, shift))


class Door(Sprite):
    def __init__(self, game, x, y, dir):

        up_img = game.spritesheet.get_image_alpha_at_col_row(2, 0)
        self.door_img = {
            "up": up_img,
            "right": pg.transform.rotate(up_img, -90),
            "down": pg.transform.rotate(up_img, 180),
            "left": pg.transform.rotate(up_img, 90)
        }
        super().__init__(game, x, y, self.door_img[dir], (game.doors, game.solid))

        self.door_hit_rect = {
            "up": (0, 0, TILE_SIZE, DOOR_THICKNESS),
            "right": (TILE_SIZE - DOOR_THICKNESS, 0,
                      DOOR_THICKNESS, TILE_SIZE),
            "down": (0, TILE_SIZE - DOOR_THICKNESS,
                     TILE_SIZE, DOOR_THICKNESS),
            "left": (0, 0, DOOR_THICKNESS, TILE_SIZE)
        }

        self.set_hit_rect(self.door_hit_rect[dir])

        self.dir = dir

        self.door_open = False

        KeyButtonTrigger(self.game, self.get_hit_rect().inflate(50, 50).move(-25,-25),
                         self.switch_door, keys=V_BUTTONS['open_door'], j_buttons=[J_BUTTONS['A']])

    def switch_door(self):
        if self.door_open:
            if not self.get_hit_rect().colliderect(self.game.player.get_hit_rect().inflate(-5, -5)):
                self.close_door()
        else:
            self.open_door()

    def close_door(self):
        self.door_open = False

        if self.dir == "left":
            self.set_dir("up")
        elif self.dir == "right":
            self.set_dir("down")
        elif self.dir == "up":
            self.set_dir("right")
        elif self.dir == "down":
            self.set_dir("left")
        else:
            assert False

        self.add(self.game.solid)
        self.game.set_visibility(self.x, self.y, False)

    def open_door(self):
        self.door_open = True

        if self.dir == "left":
            self.set_dir("down")
        elif self.dir == "right":
            self.set_dir("up")
        elif self.dir == "up":
            self.set_dir("left")
        elif self.dir == "down":
            self.set_dir("right")
        else:
            assert False

        self.remove(self.game.solid)
        self.game.set_visibility(self.x, self.y, True)

    def set_dir(self, dir):
        self.dir = dir
        self.set_image(self.door_img[dir])
        self.set_hit_rect(self.door_hit_rect[dir])

    def set_image(self, img):
        self.image = img

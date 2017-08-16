import pygame as pg
from operator import add
from settings import *
from sprites import Sprite

DOOR_THICKNESS = 8


def move(center, shift):
    return tuple(map(add, center, shift))


class Door(Sprite):
    def __init__(self, game, x, y, img, dir):
        super().__init__(game, x, y, img, (game.doors, game.solid))

        if dir == "left":
            self.hit_rect.width = DOOR_THICKNESS
            self.hit_rect.height = TILE_SIZE
        elif dir == "right":
            self.hit_rect.width = DOOR_THICKNESS
            self.hit_rect.height = TILE_SIZE
            self.hit_rect.left += TILE_SIZE - DOOR_THICKNESS
        elif dir == "up":
            self.hit_rect.width = TILE_SIZE
            self.hit_rect.height = DOOR_THICKNESS
        elif dir == "down":
            self.hit_rect.width = TILE_SIZE
            self.hit_rect.height = DOOR_THICKNESS
            self.hit_rect.top += TILE_SIZE - DOOR_THICKNESS
        else:
            print("unexpected door direction")
            assert False

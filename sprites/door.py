import pygame as pg
from operator import add
from settings import *

DOOR_THICKNESS = 8


def move(center, shift):
    return tuple(map(add, center, shift))


class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, img, dir):
        self.game = game
        self.groups = game.all_sprites, game.doors, game.solid
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = img
        self.rect = self.image.get_rect()
        if dir == "left":
            self.hit_rect = pg.Rect(0, 0, DOOR_THICKNESS, TILE_SIZE)
        elif dir == "right":
            self.hit_rect = pg.Rect(TILE_SIZE - DOOR_THICKNESS, 0, DOOR_THICKNESS, TILE_SIZE)
        elif dir == "up":
            self.hit_rect = pg.Rect(0, 0, TILE_SIZE, DOOR_THICKNESS)
        elif dir == "down":
            self.hit_rect = pg.Rect(0, TILE_SIZE - DOOR_THICKNESS, TILE_SIZE, DOOR_THICKNESS)
        else:
            print("unexpected door direction")
            assert False

        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.hit_rect.x += x * TILE_SIZE
        self.hit_rect.y += y * TILE_SIZE

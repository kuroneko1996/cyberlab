import pygame as pg
from settings import *


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.game = game

        groups = game.all_sprites, game.solid
        pg.sprite.Sprite.__init__(self, groups)

        self.image = img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

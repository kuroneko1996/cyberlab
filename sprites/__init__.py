import pygame as pg
from settings import *


class Sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, img, groups = ()):
        self.game = game

        self.groups = groups, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.image = img
        self.rect = self.image.get_rect()
        self.hit_rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.hit_rect.x = x * TILE_SIZE
        self.hit_rect.y = y * TILE_SIZE

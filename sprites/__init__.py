import pygame as pg
from settings import *
from math import sqrt


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

    def on_hit(self):
        pass

    def distance(self, sprite):
        """Returns the distance between the hit_rect centers of self and sprite"""
        return sqrt((self.hit_rect.x - sprite.hit_rect.x) ** 2
                    + (self.hit_rect.y - sprite.hit_rect.y) ** 2)

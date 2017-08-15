import pygame as pg
from settings import *


class Item(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.game = game
        # TODO create a method to change this dynamically
        self.groups = game.all_sprites, game.items_on_floor
        pg.sprite.Sprite.__init__(self, self.groups)
        #
        self.image = img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

        self.pickable = None

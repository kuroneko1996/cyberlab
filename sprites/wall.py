import pygame as pg
from settings import *
from sprites import Sprite


class Wall(Sprite):
    def __init__(self, game, x, y, img):
        super().__init__(game, x, y, img, game.solid)

import pygame as pg
from settings import *


class Camera:
    def __init__(self, width, height):
        self.rect = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def transform(self, sprite):
        return sprite.get_rect().move(self.rect.topleft)

    def transform_xy(self, x, y):
        return self.rect.left + x, self.rect.top + y

    # move camera in opposite direction
    def update(self, target):
        x = -target.get_rect().x + int(SCREEN_WIDTH / 2)
        y = -target.get_rect().y + int(SCREEN_HEIGHT / 2)

        # limit scrolling near borders of map
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(SCREEN_WIDTH - self.width, x)  # right
        y = max(SCREEN_HEIGHT - self.height, y)  # height

        updated = False
        if self.rect.x != x or self.rect.y != y or self.rect.width != self.width or self.rect.height != self.height:
            updated = True

        self.rect.x = x
        self.rect.y = y
        self.rect.width = self.width
        self.rect.height = self.height

        return updated

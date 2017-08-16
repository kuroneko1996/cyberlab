import pygame as pg


class Spritesheet:
    def __init__(self, filename):
        self.sheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

    def get_image_alpha(self, x, y, width, height):
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

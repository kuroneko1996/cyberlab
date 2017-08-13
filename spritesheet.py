import pygame as pg

class Spritesheet:
    def __init__(self, filename):
        self.sheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image

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

    def get_image_at_row_col(self, col, row):
        return self.get_image(col * 32, row * 32, 32, 32)

    def get_image_alpha_at_row_col(self, col, row):
        return self.get_image_alpha(col * 32, row * 32, 32, 32)

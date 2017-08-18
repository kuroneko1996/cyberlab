import pygame as pg
from settings import *
from .collision import *


class Sprite(pg.sprite.Sprite):
    """
    A visible game entry that is positioned on the map
    """
    def __init__(self, game, x, y, img, groups = ()):
        """
        Construct a new sprite

        :param game: game in which this sprite is loaded
        :param x: x coordinate of the sprite
        :param y: y coordinate of the sprite
        :param img: image of the sprite
        :param groups: groups of the sprite
        """
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
        """
        This method is called each time something hits this sprite
        """
        pass

    def move(self, dx, dy, do_slither=True):
        """
        Moves this sprite by (x,y), checking for collisions

        :param dx: x shift
        :param dy: y shift
        :return: true if movement succeeded, false otherwise
        """

        if can_walk(self, self.game.solid, dx, dy):
            self.x += dx
            self.y += dy

            # move on x
            self.hit_rect.x = self.x * TILE_SIZE
            hit = collide_with_map(self, self.game.solid, 'x')
            if hit and do_slither:
                slither(self.game.solid, hit, self, "y", False)

            # move on y
            self.hit_rect.y = self.y * TILE_SIZE
            hit = collide_with_map(self, self.game.solid, 'y')
            if hit and do_slither:
                slither(self.game.solid, hit, self, "x", False)

            # update image rect
            self.rect.center = self.hit_rect.center

            return True
        else:
            return False

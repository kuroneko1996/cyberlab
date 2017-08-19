import pygame as pg
from settings import *
from .collision import *


class Sprite(pg.sprite.Sprite):
    """
    A visible game entry that is positioned on the map
    """

    def __init__(self, game, x, y, img, groups=()):
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
        self.x = x
        self.y = y

        self.hit_rect = self.image.get_rect()
        self.hit_rect.x = 0
        self.hit_rect.y = 0

    def on_hit(self):
        """
        This method is called each time something hits this sprite
        """
        pass

    def get_rect(self):
        """
        Gets the image rectangle in the world coordinates
        :return: image rectangle positioned in the world coordinates
        """
        return pg.Rect(self.x * TILE_SIZE,
                       self.y * TILE_SIZE,
                       self.image.get_rect().x,
                       self.image.get_rect().y)

    def get_hit_rect(self):
        """
        Produce the hit rectangle in the world coordinates
        :return: hit rectangle positioned in the world coordinates
        """
        return self.hit_rect.move(self.x * TILE_SIZE, self.y * TILE_SIZE)

    def move(self, dx, dy):
        """
        Moves this sprite by (x,y), checking for collisions

        :param dx: x shift
        :param dy: y shift
        :return: true if movement succeeded, false otherwise
        """

        if not get_obstacles(self, self.game.solid, dx, dy):
            self.x += dx
            self.y += dy
            return True
        else:
            return False

    def set_position(self, x, y):
        """
        Sets the position of this sprite explicitly
        :param x: x coordinate in tile units
        :param y: y coordinate in tile units
        :return: nothing
        """
        self.x = x
        self.y = y

    def set_hit_rect(self, hit_rect):
        """
        Sets the hit rectangle for this sprite in the sprite's local coordinates
        :param hit_rect: new hit rectangle
        :return: nothing
        """
        self.hit_rect.left = hit_rect[0]
        self.hit_rect.top = hit_rect[1]
        self.hit_rect.width = hit_rect[2]
        self.hit_rect.height = hit_rect[3]
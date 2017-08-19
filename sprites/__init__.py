import pygame as pg
from .collision import *
# Threshold for the sign function
THRESHOLD = 0.000000001


def sgn(num):
    """
    Produce the sign of the number
    :param num: signed number
    :return: sign of the number
    """
    if num > THRESHOLD:
        return 1
    elif num < - THRESHOLD:
        return -1
    else:
        return 0

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

        self.__hit_rect = self.image.get_rect()
        self.__hit_rect.x = 0
        self.__hit_rect.y = 0

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
        return self.__hit_rect.move(self.x * TILE_SIZE, self.y * TILE_SIZE)

    def move(self, dx, dy):
        """
        Moves this sprite by (x,y), checking for collisions

        :param dx: x shift
        :param dy: y shift
        :return: true if movement succeeded (or partially succeeded),
         false otherwise
        """

        if not self.get_obstacles(dx, dy):
            self.x += dx
            self.y += dy
            return True
        else:
            if not self.get_obstacles(dx, 0):
                self.x += dx
                return True
            elif not self.get_obstacles(0, dy):
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

    def get_obstacles(self, dx, dy):
        """
        Produces obstacles in the way of sprite's movement
        :param sprite: sprite that is being moved
        :param group: clipping group
        :param dx: x shift
        :param dy: y shift
        :return: obstacles in the way of sprite's movement
        """

        return [s for s in self.game.solid if
                self.get_hit_rect()
                    .move(3 * sgn(dx), 3 * sgn(dy))
                    .colliderect(s.get_hit_rect())]

    def set_hit_rect(self, hit_rect):
        """
        Sets the hit rectangle for this sprite in the sprite's local coordinates
        :param hit_rect: new hit rectangle
        :return: nothing
        """
        self.__hit_rect.left = hit_rect[0]
        self.__hit_rect.top = hit_rect[1]
        self.__hit_rect.width = hit_rect[2]
        self.__hit_rect.height = hit_rect[3]
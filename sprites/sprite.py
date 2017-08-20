import pygame as pg
from settings import TILE_SIZE, SLITHER_SPEED
from misc import sgn


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
        :param dx: x shift
        :param dy: y shift
        :return: obstacles in the way of sprite's movement
        """

        return [s for s in self.game.solid if
                self.get_hit_rect()
                    .move(3 * sgn(dx), 3 * sgn(dy))
                    .colliderect(s.get_hit_rect())]

    # TODO: get rid of direction
    def there_is_space(self, sprite, direction):
        """
        Returns true if there is space in the direction given
        :param sprite: sprite around which to search for space
        :param direction:
        :return:
        """
        if direction == "up":
            point = (sprite.get_hit_rect().x, sprite.get_hit_rect().y - 1)
        elif direction == "down":
            point = (sprite.get_hit_rect().x, sprite.get_hit_rect().y + sprite.get_hit_rect().height + 1)
        elif direction == "right":
            point = (sprite.get_hit_rect().x + sprite.get_hit_rect().width + 1, sprite.get_hit_rect().y)
        elif direction == "left":
            point = (sprite.get_hit_rect().x - 1, sprite.get_hit_rect().y)
        else:
            assert False

        hits = [s for s in self.game.solid if s.get_hit_rect().collidepoint(point)]

        return not hits

    def slither(self, direction):
        """Slithers the sprite along the hit in the direction with an opening"""
        if direction == "right":
            hits = self.get_obstacles(1, 0)
        elif direction == "left":
            hits = self.get_obstacles(-1, 0)
        elif direction == "up":
            hits = self.get_obstacles(0, -1)
        elif direction == "down":
            hits = self.get_obstacles(0, 1)
        else:
            assert False

        if hits:
            hit = hits[0]
            if direction == "right" or "left":
                if self.there_is_space(hit, "up"):
                    self.y += SLITHER_SPEED
                elif self.there_is_space(hit, "down"):
                    self.y -= SLITHER_SPEED
            elif direction == "up" or "down":
                if self.there_is_space(hit, "right"):
                    self.x += SLITHER_SPEED
                elif self.there_is_space(hit, "left"):
                    self.x -= SLITHER_SPEED

    def collide_with_triggers(self):
        hits = [s for s in self.game.triggers if self.get_rect().inflate(20, 20).colliderect(s.hit_rect)]
        for hit in hits:
            hit.on_hit()

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
from .sprite import Sprite


class ActiveSprite(Sprite):
    """
    A sprite that can be moved dynamically
    """
    def __init__(self, game, x, y, img):
        super().__init__(game, x, y, img)
        self.vx, self.vy = 0, 0

    def move(self, dx, dy):
        """
        Moves this sprite by (x,y), checking for collisions

        Sprite also can be moved by changing x and y fields directly

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
            elif not self.get_obstacles(0, dy):
                self.y += dy
                return True
            else:
                return False

    def is_moving(self):
        """
        Checks if player is moving
        :return: true if player is moving, false otherwise
        """
        return self.vx != 0 or self.vy != 0
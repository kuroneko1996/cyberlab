from .sprite import Sprite


class Wall(Sprite):
    def __init__(self, game, x, y, img):
        super().__init__(game, x, y, img, game.solid)

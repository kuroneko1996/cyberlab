from sprites import Sprite
from settings import TILE_SIZE


class Item(Sprite):
    def __init__(self, game, x, y, img):
        super().__init__(game, x, y, img, game.items_on_floor)

        self.pickable = None

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

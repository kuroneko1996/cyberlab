import json
from settings import *


class Map:
    def __init__(self, filename):
        with open(filename, 'rt') as f:
            self.data = json.loads(f.read())

        self.width = max(map(lambda node: node["x"], self.data)) + 1 \
                     - min(map(lambda node: node["x"], self.data))
        self.height = max(map(lambda node: node["y"], self.data)) + 1 \
                      - min(map(lambda node: node["y"], self.data))
        self.on_update_screen()

    def on_update_screen(self):
        self.width_screen = self.width * TILE_SIZE
        self.height_screen = self.height * TILE_SIZE

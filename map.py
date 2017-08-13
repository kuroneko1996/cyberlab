from settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.width = len(self.data[0])
        self.height = len(self.data)
        self.on_update_screen()

    def on_update_screen(self):
        self.width_screen = self.width * TILE_SIZE
        self.height_screen = self.height * TILE_SIZE

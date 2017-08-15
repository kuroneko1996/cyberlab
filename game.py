import sys
from os import path
import pygame as pg
from settings import *
from spritesheet import Spritesheet
from sprites.player import Player
from sprites.wall import Wall
from sprites.item import Item
from pickable import Pickable
from camera import *
from map import *


class Game:
    def __init__(self):
        self.display = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)

        self.all_sprites = None
        self.spritesheet = None
        self.walls = None
        self.items_on_floor = None
        self.map = None
        self.player = None
        self.camera = None
        self.playing = False
        self.dt = 0.0

    def load(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.items_on_floor = pg.sprite.Group()

        assets_folder = path.join(path.dirname(__file__), 'assets')
        self.map = Map(path.join(assets_folder, 'maps/map1.json'))

        self.spritesheet = Spritesheet(path.join(assets_folder, 'spritesheet.png'))
        wall_img = self.spritesheet.get_image(0, 0, 32, 32)
        apple_img = self.spritesheet.get_image(32, 0, 32, 32)

        for node in self.map.data:
            if node["name"] == 'WALL':
                Wall(self, node["x"], node["y"], wall_img)
            elif node["name"] == 'PLAYER':
                self.player = Player(self, node["x"], node["y"])
            elif node["name"] == 'APPLE':
                item = Item(self, node['x'], node['y'], apple_img)
                item.pickable = Pickable(item, 'apple')

        self.camera = Camera(self.map.width_screen, self.map.height_screen)

    def update(self):
        for sprite in self.all_sprites:
            sprite.update(self.dt)

        self.camera.update(self.player)

    def draw(self):
        self.display.fill(BG_COLOR)

        # TODO layering
        for sprite in self.all_sprites:
            if sprite != self.player:
                self.display.blit(sprite.image, self.camera.transform(sprite))

        self.display.blit(self.player.image, self.camera.transform(self.player))

        # pg.draw.rect(self.display, (0,255,0), self.player.hit_rect, 1)
        # pg.draw.rect(self.display, (255, 255, 255), self.player.rect, 1)
        pg.display.flip()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_F11:
                    self.toggle_fullscreen()

    def toggle_fullscreen(self):
        """Taken from http://pygame.org/wiki/toggle_fullscreen"""

        screen = pg.display.get_surface()
        tmp = screen.convert()
        caption = pg.display.get_caption()
        cursor = pg.mouse.get_cursor()

        w, h = screen.get_width(), screen.get_height()
        flags = screen.get_flags()
        bits = screen.get_bitsize()

        pg.display.quit()
        pg.display.init()

        self.display = pg.display.set_mode((w, h), flags ^ pg.FULLSCREEN, bits)
        self.display.blit(tmp, (0, 0))
        pg.display.set_caption(*caption)

        pg.key.set_mods(0)

        pg.mouse.set_cursor(*cursor)

        return screen

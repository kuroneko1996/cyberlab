import sys
from os import path
import pygame as pg
from settings import *
from spritesheet import Spritesheet
from sprites.player import Player
from sprites.wall import Wall
from sprites.item import Item
from sprites.door import Door
from pickable import Pickable
from triggers.trigger import *
from camera import *
from map import *


class Game:
    def __init__(self, display):
        self.display = display
        self.clock = pg.time.Clock()
        pg.display.set_caption(WINDOW_TITLE)

        self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
        self.joystick = None
        if len(self.joysticks) > 0:
            self.joystick = self.joysticks[0]
            self.joystick.init()

        # sprite groups
        self.all_sprites = None
        self.items_on_floor = None
        self.solid = None
        self.doors = None

        self.triggers = []
        self.spritesheet = None
        self.map = None
        self.player = None
        self.camera = None
        self.playing = False
        self.dt = 0.0
        self.keys_just_pressed = {}

        self.textBox = pg.image.load("assets/textBox.png").convert_alpha()
        self.font = pg.font.Font("assets/fonts/Arcon.otf", 20)
        self.fontSpace = pg.font.Font("assets/fonts/Arcon.otf", 14)
        self.showTextBox = False
        self.text = None

    def load(self):
        self.all_sprites = pg.sprite.Group()
        self.solid = pg.sprite.Group()
        self.items_on_floor = pg.sprite.Group()
        self.doors = pg.sprite.Group()

        assets_folder = path.join(path.dirname(__file__), 'assets')
        self.map = Map(path.join(assets_folder, 'maps/map1.json'))

        self.spritesheet = Spritesheet(path.join(assets_folder, 'spritesheet.png'), 32)
        wall_img = self.spritesheet.get_image_at_row_col(0, 0)
        apple_img = self.spritesheet.get_image_alpha_at_row_col(1, 0)

        for node in self.map.objects:
            if node["name"] == 'WALL':
                Wall(self, node["x"], node["y"], wall_img)
            elif node["name"] == 'PLAYER':
                self.player = Player(self, node["x"], node["y"])
            elif node["name"] == 'APPLE':
                item = Item(self, node['x'], node['y'], apple_img)
                item.pickable = Pickable(item, 'apple', False, 1, False)
            elif node["name"] == "DOOR":
                door = Door(self, node["x"], node["y"], node["dir"])
                KeyButtonTrigger(self, door.rect.inflate(20, 20), door.switch_door, pg.K_RETURN)

        for trigger in self.map.triggers:
            TextTrigger(self,
                        pg.Rect(trigger["x"], trigger["y"], trigger["width"], trigger["height"]),
                        trigger["text"])

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
        if self.showTextBox is True:
            self.bot_message(self.text)

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
        self.keys_just_pressed.clear()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                self.keys_just_pressed[event.key] = True
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

    def key_just_pressed(self, key):
        if key in self.keys_just_pressed:
            return True
        return False

    def get_axis(self, number):
        if self.joystick is not None:
            return self.joystick.get_axis(number)
        return 0.0

    def bot_message(self, text):
        self.display.blit(self.textBox, (0, 360))
        self.display.blit(self.font.render(text, True, (255, 255, 255)), (150, 390))
        self.display.blit(self.fontSpace.render("[SPACE]", True, (255, 255, 255)), (560, 440))
        pg.display.flip()

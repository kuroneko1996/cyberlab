import sys
from os import path, getcwd
import math
from spritesheet import Spritesheet
from sprites.player import Player
from sprites.wall import Wall
from sprites.item import Item
from sprites.door import Door
from pickable import Pickable
from nanogui import Nanogui
from triggers import *
from camera import *
from map import *
from fov import calc_fov


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
        self.joystick_just_pressed = {}

        self.textBox = pg.image.load("assets/textBox.png").convert_alpha()
        self.font = pg.font.Font("assets/fonts/Arcon.otf", 20)
        self.fontSpace = pg.font.Font("assets/fonts/Arcon.otf", 14)
        self.showTextBox = False
        self.text = None

        self.gui = Nanogui()
        self.visibility_data = None  # [x][y] -> True, False
        self.fov_data = None  # [x][y] -> True, False
        self.update_fov = True

    def load(self):
        self.all_sprites = pg.sprite.Group()
        self.solid = pg.sprite.Group()
        self.items_on_floor = pg.sprite.Group()
        self.doors = pg.sprite.Group()

        assets_folder = path.join(getcwd(), 'assets')
        self.map = Map(path.join(assets_folder, 'maps/map1.json'))

        self.spritesheet = Spritesheet(path.join(assets_folder, 'spritesheet.png'), 32)
        wall_img = self.spritesheet.get_image_at_row_col(0, 0)
        apple_img = self.spritesheet.get_image_alpha_at_row_col(1, 0)

        self.visibility_data = [[True] * self.map.height for i in range(self.map.width)]
        self.fov_data = [[True] * self.map.height for i in range(self.map.width)]

        for node in self.map.objects:
            x, y = node['x'], node['y']
            if node["name"] == 'WALL':
                Wall(self, x, y, wall_img)
                self.visibility_data[x][y] = False
            elif node["name"] == 'PLAYER':
                self.player = Player(self, x, y)
            elif node["name"] == 'APPLE':
                item = Item(self, x, y, apple_img)
                item.pickable = Pickable(item, 'apple', False, 1, False)
            elif node["name"] == "DOOR":
                Door(self, x, y, node["dir"])
                self.visibility_data[x][y] = False  # TODO opened doors visibility

        for trigger in self.map.triggers:
            TextTrigger(self,
                        pg.Rect(trigger["x"], trigger["y"], trigger["width"], trigger["height"]),
                        trigger["text"])

        self.camera = Camera(self.map.width_screen, self.map.height_screen)

    def update(self):
        self.gui.pre(self.joystick)

        for sprite in self.all_sprites:
            sprite.update(self.dt)

        if self.camera.update(self.player) or self.update_fov:
            player_hit_rect = self.player.get_hit_rect()
            player_tilex = math.floor(player_hit_rect.x / TILE_SIZE)
            player_tiley = math.floor(player_hit_rect.y / TILE_SIZE)

            self.fov_data = calc_fov(player_tilex, player_tiley, FOV_RADIUS,
                                     self.visibility_data, self.fov_data)
            self.update_fov = False

        self.gui.after()

    def draw(self):
        self.display.fill(BG_COLOR)

        # TODO layering
        for sprite in self.all_sprites:
            if sprite != self.player and not isinstance(sprite, Item):
                self.display.blit(sprite.image, self.camera.transform(sprite))

        for sprite in self.items_on_floor:
            tilex = math.floor(sprite.x)
            tiley = math.floor(sprite.y)
            if self.fov_data[tilex][tiley]:
                self.display.blit(sprite.image, self.camera.transform(sprite))

        if DEBUG_FOV:
            self.draw_fov()

        self.display.blit(self.player.image, self.camera.transform(self.player))
        if self.showTextBox is True:
            self.bot_message(self.text)

        self.gui.draw()
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
        self.joystick_just_pressed.clear()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                self.keys_just_pressed[event.key] = True
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_F11:
                    self.toggle_fullscreen()
            if event.type == pg.JOYBUTTONDOWN:
                self.joystick_just_pressed[event.button] = True

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

    def get_key_jp(self, key):
        # get key just pressed (clears on new frame)
        if key in self.keys_just_pressed:
            return True
        return False

    def get_joystick_jp(self, button):
        # get joystick button just pressed (clears on new frame)
        if button in self.joystick_just_pressed:
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

    def set_visibility(self, tilex, tiley, value):
        self.visibility_data[tilex][tiley] = value
        self.update_fov = True

    def draw_fov(self):
        for x in range(len(self.fov_data)):
            for y in range(len(self.fov_data[0])):
                if self.fov_data[x][y]:
                    newx, newy = self.camera.transform_xy(x * TILE_SIZE, y * TILE_SIZE)
                    pg.draw.rect(self.display, (200, 200, 200), pg.Rect(newx, newy,
                                                                        TILE_SIZE, TILE_SIZE), 1)

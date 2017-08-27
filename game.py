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

        # Contains messages to be displayed on the player's screen
        self.message_queue = []

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

        self.background_surface = None
        self.triggers = []
        self.collisions = []  # rectangles
        self.spritesheet = None
        self.map = None
        self.player = None
        self.camera = None
        self.playing = False
        self.dt = 0.0
        self.global_time = 0
        self.pressed_keys = {}
        self.keys_just_pressed = {}
        self.joystick_just_pressed = {}

        self.gui = Nanogui(display)
        self.visibility_data = None  # [x][y] -> True, False
        self.fov_data = None  # [x][y] -> True, False
        self.update_fov = True
        self.light_map = []

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
        self.background_surface = pg.Surface((self.map.width * TILE_SIZE, self.map.height * TILE_SIZE))

        self.visibility_data = [[True] * self.map.height for i in range(self.map.width)]
        self.fov_data = [[True] * self.map.height for i in range(self.map.width)]

        for node in self.map.objects:
            x, y = node['x'], node['y']
            if node["name"] == 'WALL':
                #self.collisions.append(pg.Rect(x, y, TILE_SIZE, TILE_SIZE))  # TODO big rectangles
                wall = Wall(self, x, y, wall_img)
                wall.remove(self.all_sprites)  # skip drawing
                self.background_surface.blit(wall_img, (x * TILE_SIZE, y * TILE_SIZE))
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

        self.player.update(self.dt)

        camera_updated = self.camera.update(self.player)
        if self.update_fov:
            player_hit_rect = self.player.get_hit_rect()
            player_tilex = math.floor(player_hit_rect.x / TILE_SIZE)
            player_tiley = math.floor(player_hit_rect.y / TILE_SIZE)

            self.fov_data = calc_fov(player_tilex, player_tiley, FOV_RADIUS,
                                     self.visibility_data, self.fov_data)
            self.update_light_map(self.player.x, self.player.y)
            self.update_fov = False

        if self.message_queue:
            if self.global_time % TYPING_SPEED < self.dt:
                self.message_queue[-1].type_more()

        self.gui.after()

    def draw(self):
        self.display.fill(BG_COLOR)

        bg_x, bg_y = self.camera.transform_xy(0, 0)
        self.display.blit(self.background_surface, (bg_x, bg_y))

        # TODO layering
        for sprite in self.all_sprites:
            if sprite != self.player and not isinstance(sprite, Item):
                self.display.blit(sprite.image, self.camera.transform(sprite))

        for sprite in self.items_on_floor:
            tilex = math.floor(sprite.x)
            tiley = math.floor(sprite.y)
            if self.fov_data[tilex][tiley]:
                self.display.blit(sprite.image, self.camera.transform(sprite))

        # darken image
        self.display.fill(DARKEN_COLOR, special_flags=pg.BLEND_SUB)
        # draw light
        for light in self.light_map:
            self.display.fill(light[1], light[0], pg.BLEND_ADD)

        if DEBUG_FOV:
            self.draw_fov()

        self.display.blit(self.player.image, self.camera.transform(self.player))
        if self.message_queue:
            self.message_queue[-1].render(self.display)

            #self.__put_text_on_screen__(str(message))
            #if message.has_picture():
            #    self.__put_picture_on_screen__(message.get_picture())

        self.gui.draw()
        pg.display.flip()

    def __put_picture_on_screen__(self, image):
        self.display.blit(image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.global_time += self.dt
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        self.keys_just_pressed.clear()
        self.joystick_just_pressed.clear()

        self.pressed_keys = pg.key.get_pressed()
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

    def get_vbutton_down(self, name):
        if name in V_BUTTONS:
            for key in V_BUTTONS[name]:
                if self.pressed_keys[key]:
                    return True
        return False

    def get_vbutton_jp(self, name):
        if name in V_BUTTONS:
            for key in V_BUTTONS[name]:
                if key in self.keys_just_pressed:
                    return True
        return False

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

    def update_light_map(self, source_x, source_y):
        self.light_map.clear()
        radius_sqr = FOV_RADIUS * FOV_RADIUS
        tmp = 1.0 / (1.0 + radius_sqr)

        for x in range(len(self.fov_data)):
            for y in range(len(self.fov_data[0])):
                if self.fov_data[x][y]:
                    newx, newy = self.camera.transform_xy(x * TILE_SIZE, y * TILE_SIZE)

                    dist_sqr = (source_x - x)*(source_x - x) + (source_y - y)*(source_y - y)
                    intensity = 1.0 / (1.0 + dist_sqr / 20)
                    intensity = intensity - tmp
                    intensity = intensity / (1.0 - tmp)
                    color = tuple(intensity*v for v in LIGHT_COLOR)
                    self.light_map.append((pg.Rect(newx, newy, TILE_SIZE, TILE_SIZE), color))

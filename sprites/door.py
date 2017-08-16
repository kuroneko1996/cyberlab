from operator import add
from settings import *
from sprites import Sprite
import pygame as pg

DOOR_THICKNESS = 8


def move(center, shift):
    return tuple(map(add, center, shift))


class Door(Sprite):
    def __init__(self, game, x, y, dir):
        self.door_img = {
            "up": game.spritesheet.get_image_alpha_at_row_col(2, 0),
            "right": game.spritesheet.get_image_alpha_at_row_col(3, 0),
            "down": game.spritesheet.get_image_alpha_at_row_col(4, 0),
            "left": game.spritesheet.get_image_alpha_at_row_col(5, 0)
        }
        super().__init__(game, x, y, self.door_img[dir], (game.doors, game.solid))

        self.door_hit_rect = {
            "up": (self.hit_rect.left, self.hit_rect.top, TILE_SIZE, DOOR_THICKNESS),
            "right": (self.hit_rect.left + TILE_SIZE - DOOR_THICKNESS,
                      self.hit_rect.top, DOOR_THICKNESS, TILE_SIZE),
            "down": (self.hit_rect.left, self.hit_rect.top + TILE_SIZE - DOOR_THICKNESS,
                     TILE_SIZE, DOOR_THICKNESS),
            "left": (self.hit_rect.left, self.hit_rect.top, DOOR_THICKNESS, TILE_SIZE)
        }

        self.set_hit_rect(self.door_hit_rect[dir])

        self.dir = dir

        self.door_open = False

    def on_hit(self):
        if pg.K_RETURN in self.game.keys_just_pressed:
            self.switch_door()

    def switch_door(self):
        if self.door_open:
            if not self.rect.colliderect(self.game.player.hit_rect.inflate(-10, -10)):
                self.close_door()
        else:
            self.open_door()

    def close_door(self):
        self.door_open = False

        if self.dir == "left":
            self.set_dir("up")
        elif self.dir == "right":
            self.set_dir("down")
        elif self.dir == "up":
            self.set_dir("right")
        elif self.dir == "down":
            self.set_dir("left")
        else:
            assert False

    def open_door(self):
        self.door_open = True

        if self.dir == "left":
            self.set_dir("down")
        elif self.dir == "right":
            self.set_dir("up")
        elif self.dir == "up":
            self.set_dir("left")
        elif self.dir == "down":
            self.set_dir("right")
        else:
            assert False

    def set_dir(self, dir):
        self.dir = dir
        self.set_image(self.door_img[dir])
        self.set_hit_rect(self.door_hit_rect[dir])

    def set_image(self, img):
        self.image = img
        new_rect = self.image.get_rect()
        self.rect.width = new_rect.width
        self.rect.height = new_rect.height

    def set_hit_rect(self, hit_rect_builder):
        self.hit_rect.left = hit_rect_builder[0]
        self.hit_rect.top = hit_rect_builder[1]
        self.hit_rect.width = hit_rect_builder[2]
        self.hit_rect.height = hit_rect_builder[3]

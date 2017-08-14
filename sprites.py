import pygame as pg
from settings import *


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_map(sprite, group, axis):
    if axis == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vx > 0:
                sprite.x = hits[0].rect.left - sprite.hit_rect.width
            elif sprite.vx < 0:
                sprite.x = hits[0].rect.right
            sprite.vx = 0
            sprite.hit_rect.x = sprite.x
    elif axis == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if sprite.vy > 0:
                sprite.y = hits[0].rect.top - sprite.hit_rect.height
            elif sprite.vy < 0:
                sprite.y = hits[0].rect.bottom
            sprite.vy = 0
            sprite.hit_rect.y = sprite.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = img

        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 16, 30)
        self.hit_rect.center = self.rect.center

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.vx, self.vy = 0, 0
        self.spd = 200

    def input(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.spd
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.spd
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.spd
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.spd

        # diagonals
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.707
            self.vy *= 0.707



    def update(self, dt):
        self.input()

        self.x += self.vx * dt
        self.y += self.vy * dt
        # move on x
        self.hit_rect.x = self.x
        collide_with_map(self, self.game.walls, 'x')
        # move on y
        self.hit_rect.y = self.y
        collide_with_map(self, self.game.walls, 'y')
        # update image rect
        self.rect.center = self.hit_rect.center

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.game = game
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

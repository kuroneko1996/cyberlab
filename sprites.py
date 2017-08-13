import pygame as pg
from settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, img):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = img

        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 16, 32)
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

    def collide_with_map(self, axis):
        if axis == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.hit_rect.width
                elif self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.hit_rect.x = self.x
        elif axis == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.hit_rect.height
                elif self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.hit_rect.y = self.y

    def update(self, dt):
        self.input()

        self.x += self.vx * dt
        self.y += self.vy * dt
        # move on x
        self.hit_rect.x = self.x
        self.collide_with_map('x')
        # move on y
        self.hit_rect.y = self.y
        self.collide_with_map('y')
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

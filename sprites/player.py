import pygame as pg
from settings import *
from animation import Animation, PlayMode
from container import Container
from .collision import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.idle_image = game.spritesheet.get_image_alpha(0, 32, 32, 32)

        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, 16, 30)
        self.hit_rect.center = self.rect.center

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.vx, self.vy = 0, 0
        self.spd = 200
        self.last_movex = 0.0
        self.last_movey = 0.0
        self.moving = False

        self.animation_timer = 0.0
        self.idling_animation = Animation(
            0.50, PlayMode.LOOP,
            game.spritesheet.get_image_alpha(0, 32, 32, 32),
            game.spritesheet.get_image_alpha(32, 32, 32, 32)
        )
        self.walking_animation_up = Animation(
            0.10, PlayMode.LOOP,
            game.spritesheet.get_image_alpha(64, 32, 32, 32),
            game.spritesheet.get_image_alpha(96, 32, 32, 32),
            game.spritesheet.get_image_alpha(128, 32, 32, 32)
        )
        self.walking_animation_down = Animation(
            0.10, PlayMode.LOOP,
            game.spritesheet.get_image_alpha(160, 32, 32, 32),
            game.spritesheet.get_image_alpha(192, 32, 32, 32),
            game.spritesheet.get_image_alpha(224, 32, 32, 32)
        )
        self.walking_animation_left = Animation(
            0.10, PlayMode.LOOP,
            game.spritesheet.get_image_alpha(64, 64, 32, 32),
            game.spritesheet.get_image_alpha(96, 64, 32, 32),
            game.spritesheet.get_image_alpha(128, 64, 32, 32)
        )
        self.walking_animation_right = Animation(
            0.10, PlayMode.LOOP,
            game.spritesheet.get_image_alpha(160, 64, 32, 32),
            game.spritesheet.get_image_alpha(192, 64, 32, 32),
            game.spritesheet.get_image_alpha(224, 64, 32, 32)
        )

        self.container = Container(self, 16)

    def input(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.spd
            self.last_movex = -1
            self.last_movey = 0
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.spd
            self.last_movex = 1
            self.last_movey = 0
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.spd
            self.last_movey = -1
            self.last_movex = 0
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.spd
            self.last_movey = 1
            self.last_movex = 0

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

        if self.vx != 0 or self.vy != 0:
            self.moving = True
        else:
            self.moving = False

        self.auto_pick_up_items()
        self.update_animation(dt)

    def update_animation(self, dt):
        self.image = self.idling_animation.get_key_frame(self.animation_timer)

        if self.moving and self.last_movey != 0:
            if self.last_movey > 0:
                self.image = self.walking_animation_up.get_key_frame(self.animation_timer)
            else:
                self.image = self.walking_animation_down.get_key_frame(self.animation_timer)
        elif self.moving and self.last_movex != 0:
            if self.last_movex > 0:
                self.image = self.walking_animation_right.get_key_frame(self.animation_timer)
            else:
                self.image = self.walking_animation_left.get_key_frame(self.animation_timer)

        self.animation_timer += dt
        if self.animation_timer >= 60:
            self.animation_timer = 0.0

    def auto_pick_up_items(self):
        items = pg.sprite.spritecollide(self, self.game.items_on_floor, False)
        for item in items:
            if item.pickable is not None:
                print("picked up:", item.pickable.id, "x", item.pickable.amount)
                self.container.add(item.pickable)
                self.game.all_sprites.remove(item)  # TODO move to pickable.py?
                self.game.items_on_floor.remove(item)

import pygame as pg
from settings import *
from animation import Animation, PlayMode
from container import Container
from .collision import *
from sprites import Sprite

HITBOX_DOWN_SHIFT = -8


class Player(Sprite):
    def __init__(self, game, x, y):
        self.idle_image = game.spritesheet.get_image_alpha(0, TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.image = self.idle_image
        super().__init__(game, x, y, self.image)

        self.hit_rect.width = TILE_SIZE/2
        self.hit_rect.height = TILE_SIZE / 2

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

        if self.game.key_just_pressed(pg.K_q):
            self.drop_item()
        elif self.game.key_just_pressed(pg.K_g) or self.game.key_just_pressed(pg.K_e):
            self.pickup_items()
        if self.game.key_just_pressed(pg.K_SPACE):
            self.game.showTextBox = False

    def update(self, dt):
        self.input()

        self.x += self.vx * dt
        self.y += self.vy * dt
        # move on x
        self.hit_rect.x = self.x
        collide_with_map(self, self.game.solid, 'x')
        # move on y
        self.hit_rect.y = self.y
        collide_with_map(self, self.game.solid, 'y')
        # update image rect
        self.rect.center = self.hit_rect.center
        self.rect = self.rect.move(0, HITBOX_DOWN_SHIFT)

        if self.vx != 0 or self.vy != 0:
            self.moving = True
        else:
            self.moving = False

        self.pickup_items(True)
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

    def pickup_items(self, auto_pick=False):
        items = pg.sprite.spritecollide(self, self.game.items_on_floor, False)
        for item in items:
            if item.pickable is not None:
                if auto_pick is True and item.pickable.auto_pick is False:
                    continue
                print("picked up:", item.pickable.id, "x", item.pickable.amount)
                self.game.text = "Picking up "+item.pickable.id+" ..."
                self.game.showTextBox = True
                # TODO move to pickable.py?
                self.container.add(item.pickable)
                item.remove(self.game.all_sprites, self.game.items_on_floor)

    def drop_item(self):
        # drops first existing item
        pickable = next((value for value in self.container.inventory if value is not None), None)
        if pickable is not None:
            self.container.remove(pickable)
            item = pickable.owner
            item.set_position(self.x, self.y)
            item.add(self.game.all_sprites, self.game.items_on_floor)
            print("dropped:", item.pickable.id, "x", item.pickable.amount)
            self.game.text = "Dropping "+item.pickable.id+" ..."
            self.game.showTextBox = True

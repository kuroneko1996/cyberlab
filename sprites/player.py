import pygame as pg
import math
from settings import *
from animation import Animation, PlayMode
from container import Container
from .active_sprite import ActiveSprite

HITBOX_DOWN_SHIFT = -8


class Player(ActiveSprite):
    def __init__(self, game, x, y):
        self.idle_image = game.spritesheet.get_image_alpha_at_row_col(0, 1)
        self.image = self.idle_image
        super().__init__(game, x, y, self.image)

        self.set_hit_rect((TILE_SIZE / 4, TILE_SIZE / 2, TILE_SIZE / 2, TILE_SIZE / 2))

        self.spd = 6
        self.last_movex = 0.0
        self.last_movey = 0.0

        self.animation_timer = 0.0
        self.idling_animation = Animation(
            0.50, PlayMode.LOOP,
            game.spritesheet.get_image_alpha_at_row_col(0, 1),
            game.spritesheet.get_image_alpha_at_row_col(1, 1)
        )
        self.walking_animation_up = Animation(
            0.10, PlayMode.LOOP,
            game.spritesheet.get_image_alpha_at_row_col(2, 1),
            game.spritesheet.get_image_alpha_at_row_col(3, 1),
            game.spritesheet.get_image_alpha_at_row_col(4, 1)
        )
        self.walking_animation_down = Animation(
            0.10, PlayMode.LOOP,
            game.spritesheet.get_image_alpha_at_row_col(5, 1),
            game.spritesheet.get_image_alpha_at_row_col(6, 1),
            game.spritesheet.get_image_alpha_at_row_col(7, 1)
        )
        self.walking_animation_left = Animation(
            0.10, PlayMode.LOOP,
            game.spritesheet.get_image_alpha_at_row_col(2, 2),
            game.spritesheet.get_image_alpha_at_row_col(3, 2),
            game.spritesheet.get_image_alpha_at_row_col(4, 2)
        )
        self.walking_animation_right = Animation(
            0.10, PlayMode.LOOP,
            game.spritesheet.get_image_alpha_at_row_col(5, 2),
            game.spritesheet.get_image_alpha_at_row_col(6, 2),
            game.spritesheet.get_image_alpha_at_row_col(7, 2)
        )

        self.container = Container(self, 16)

    def input(self):
        """
        Handles the user input
        :return: true if the player has moved, false otherwise
        """

        self.vx, self.vy = 0, 0

        keys = pg.key.get_pressed()
        game = self.game

        x_axis = game.get_axis(0)
        if abs(x_axis) < JOYSTICK_THRESHOLD:
            x_axis = 0
        y_axis = game.get_axis(1)
        if abs(y_axis) < JOYSTICK_THRESHOLD:
            y_axis = 0

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            x_axis = -1
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            x_axis = 1
        if keys[pg.K_UP] or keys[pg.K_w]:
            y_axis = -1
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            y_axis = 1

        # Check for collisions
        if self.get_obstacles(self.spd * x_axis, 0):
            x_axis = 0
        if self.get_obstacles(0, self.spd * y_axis):
            y_axis = 0

        self.vx = self.spd * x_axis
        self.vy = self.spd * y_axis

        if y_axis != 0:
            self.last_movey = y_axis
            self.last_movex = 0
        elif x_axis != 0:
            self.last_movex = x_axis
            self.last_movey = 0

        # diagonals
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.707
            self.vy *= 0.707

        if game.get_key_jp(pg.K_q) or game.get_joystick_jp(J_BUTTONS['X']):
            self.drop_item()
        elif game.get_key_jp(pg.K_g) or game.get_key_jp(pg.K_e) or game.get_joystick_jp(J_BUTTONS['A']):
            self.pickup_items()
        if game.get_key_jp(pg.K_SPACE) or game.get_joystick_jp(J_BUTTONS['A']) or game.get_joystick_jp(J_BUTTONS['B']):
            game.showTextBox = False

        return self.is_moving()

    def update(self, dt):
        if self.input():
            if not self.move(self.vx * dt, self.vy * dt):
                self.vx = 0
                self.vy = 0
            else:
                self.game.update_fov = True

        self.collide_with_triggers()
        self.pickup_items(True)
        self.update_animation(dt)

    def update_animation(self, dt):
        self.image = self.idling_animation.get_key_frame(self.animation_timer)

        if self.is_moving() and self.last_movey != 0:
            if self.last_movey > 0:
                self.image = self.walking_animation_up.get_key_frame(self.animation_timer)
            else:
                self.image = self.walking_animation_down.get_key_frame(self.animation_timer)
        elif self.is_moving() and self.last_movex != 0:
            if self.last_movex > 0:
                self.image = self.walking_animation_right.get_key_frame(self.animation_timer)
            else:
                self.image = self.walking_animation_left.get_key_frame(self.animation_timer)

        self.animation_timer += dt
        if self.animation_timer >= 60:
            self.animation_timer = 0.0

    def pickup_items(self, auto_pick=False):
        items = [s for s in self.game.items_on_floor if self.get_hit_rect().colliderect(s.get_hit_rect())]
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

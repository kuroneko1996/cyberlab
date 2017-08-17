import pygame as pg


class Trigger:
    def __init__(self, game, hit_rect, callback):
        self.game = game
        self.hit_rect = hit_rect
        self.callback = callback

    def set_callback(self, callback):
        self.callback = callback

    def on_hit(self):
        if self.callback is not None:
            self.callback()


class KeyButtonTrigger(Trigger):
    def __init__(self, game, hit_rect, callback, *keys):
        self.keys = keys
        game.triggers.append(self)
        super().__init__(game, hit_rect, callback)

    def on_hit(self):
        for key in self.keys:
            if key in self.game.keys_just_pressed:
                self.callback()
                break

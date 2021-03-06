import re

from triggers.message import get_message


class Trigger:
    def __init__(self, game, hit_rect):
        self.game = game
        self.hit_rect = hit_rect
        game.triggers.append(self)

    def callback(self):
        pass

    def on_hit(self):
        self.callback()


class KeyButtonTrigger(Trigger):
    def __init__(self, game, hit_rect, callback, keys, j_buttons = None):
        self.keys = keys
        self.joystick_buttons = j_buttons
        super().__init__(game, hit_rect)
        self.callback = callback

    def on_hit(self):
        for key in self.keys:
            if key in self.game.keys_just_pressed:
                self.callback()
                return

        for button in self.joystick_buttons:
            if button in self.game.joystick_just_pressed:
                self.callback()
                return


class TextTrigger(Trigger):
    def __init__(self, game, hit_rect, text):
        super().__init__(game, hit_rect)
        self.text = text
        self.activated = False

    def callback(self):
        if not self.activated:
            for message in re.split("\n\n", self.text):
                get_message(message)
            self.activated = True

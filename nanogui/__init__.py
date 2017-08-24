import pygame as pg


class Nanogui:
    def __init__(self, display):
        self.display = display
        self.mousex = 0
        self.mousey = 0
        self.mousedown = 0
        self.jdelay = 0
        self.hot_item = 0
        self.active_item = 0

        # keyboard
        self.kbd_item = 0
        self.key_entered = 0
        self.key_shift = 0
        self.last_widget = 0

        self.draw_elements = {}

        self.font = pg.font.Font("assets/fonts/Arcon.otf", 14)
        self.font_large = pg.font.Font("assets/fonts/Arcon.otf", 32)

    def draw(self):
        if len(self.draw_elements) == 0:
            return
        for key, value in self.draw_elements.items():
            value()

    def pre(self, joystick):
        # called in update
        self.mousex, self.mousey = pg.mouse.get_pos()
        m_button1, _, _ = pg.mouse.get_pressed()
        if m_button1:
            self.mousedown = True
        else:
            self.mousedown = False

        self.draw_elements.clear()

    def after(self):
        # called in update
        if not self.mousedown:
            self.active_item = 0
        elif self.active_item == 0:
            self.active_item = -1

    def key_pressed(self, key):
        self.key_entered = key
        # TODO keyshift

    def region_hit(self, x, y, w, h):
        return not(self.mousex < x or self.mousey < y or self.mousex >= x + w or self.mousey >= y + h)

    def focus_change(self):
        if self.key_entered == pg.K_TAB or self.key_entered == pg.K_DOWN:
            self.kbd_item = 0
            self.key_entered = 0
            if self.key_shift:  # move back
                self.kbd_item = self.last_widget
            return True
        elif self.key_entered == pg.K_UP:
            self.key_entered = 0
            self.kbd_item = self.last_widget
            return True
        else:
            return False

    def label(self, id, text, x, y, color=(255, 255, 255)):
        if not(id in self.draw_elements):
            def func():
                surface = self.font.render(text, True, color)
                self.display.blit(surface, (x, y))

            self.draw_elements[id] = func

import pygame as pg
from settings import FONT, FONT_BIGGER


class Nanogui:
    def __init__(self, display):
        self.display = display
        self.mousex = 0
        self.mousey = 0
        self.mousedown = False
        self.jdelay = 0
        self.hot_item = 0
        self.active_item = 0

        # keyboard
        self.kbd_item = 0
        self.key_entered = 0
        self.key_shift = False
        self.last_widget = 0

        self.draw_elements = {}

        self.font = pg.font.Font(*FONT)
        self.font_large = pg.font.Font(*FONT_BIGGER)

    def draw(self):
        if len(self.draw_elements) == 0:
            return
        for key, value in self.draw_elements.items():
            value()

    def pre(self, joystick, mousedown=False):
        # called in update
        self.mousex, self.mousey = pg.mouse.get_pos()
        self.mousedown = bool(mousedown)

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

    def change_page(self):
        self.kbd_item = 0
        self.last_widget = 0
        self.key_entered = 0
        self.key_shift = False

    def label(self, id, text, x, y, color=(255, 255, 255)):
        if not(id in self.draw_elements):
            def draw_func():
                surface = self.font.render(text, True, color)
                self.display.blit(surface, (x, y))

            self.draw_elements[id] = draw_func

    def button(self, id, text, x, y, w=64, h=48):
        if self.region_hit(x, y, w, h):
            self.hot_item = id
            if self.active_item == 0 and self.mousedown is True:
                self.active_item = id

        # keyboard focus
        if self.kbd_item == 0:  # get focus
            self.kbd_item = id

        # creating draw function
        if not(id in self.draw_elements):
            def draw_func():
                xpos = x
                ypos = y

                if self.hot_item == id:  # hovered
                    if self.active_item == id:
                        # clicked
                        xpos = x + 4
                        ypos = y + 4
                        pg.draw.rect(self.display, (255, 255, 255), pg.Rect(xpos, ypos, w, h))
                    else:
                        pg.draw.rect(self.display, (200, 200, 200), pg.Rect(xpos, ypos, w, h))
                else:
                    pg.draw.rect(self.display, (100, 100, 100), pg.Rect(xpos, ypos, w, h))

                # text
                text_surface = self.font.render(text, True, (255, 255, 255))
                text_x = xpos + w // 2 - text_surface.get_width() // 2
                text_y = ypos + h // 2 - text_surface.get_height() // 2
                self.display.blit(text_surface, (text_x, text_y))

                if self.kbd_item == id:
                    # draw focus
                    pass

            self.draw_elements[id] = draw_func

        # focus keys
        if self.kbd_item == id:
            if not self.focus_change():
                if self.key_entered == pg.K_RETURN:
                    self.key_entered = 0
                    return True

        self.last_widget = id

        # return
        if self.mousedown is False and self.hot_item != 0 and self.active_item == id:
            return True

        return False

    def slider(self, id, value, min, max, x, y, w=256, h=32, handler_size=16):
        xpos = ((w-handler_size) * value) / max
        step = max / 10

        if self.region_hit(x, y, w + handler_size, h):
            self.hot_item = id
            if self.active_item == 0 and self.mousedown is True:
                self.active_item = id

        # keyboard focus
        if self.kbd_item == 0:
            self.kbd_item = id

        if not (id in self.draw_elements):
            def draw_func():
                pg.draw.rect(self.display, (255, 255, 255), pg.Rect(x, y, w + handler_size, h))

                # drawing handler
                if self.active_item == id or self.hot_item == id:
                    pg.draw.rect(self.display, (200, 200, 200), pg.Rect(x + 8 + xpos, y + 8, handler_size, h))
                else:
                    pg.draw.rect(self.display, (100, 100, 100), pg.Rect(x + 8 + xpos, y + 8, handler_size, h))

                if self.kbd_item == id:  # show keyboard focus
                    pass

            self.draw_elements[id] = draw_func

        # value set
        new_value = value
        # mouse
        if self.active_item == id:
            mouse_posx = self.mousex - (x + 8)
            if mouse_posx < 0:
                mouse_posx = 0
            elif mouse_posx > w:
                mouse_posx = w
            new_value = (mouse_posx * max) / w

        # keyboard
        if self.kbd_item == id:
            if not(self.focus_change()):
                if self.key_entered == pg.K_LEFT:
                    if value > 0:
                        new_value = value - step
                    self.key_entered = 0
                elif self.key_entered == pg.K_RIGHT:
                    if value < max:
                        new_value = value + step
                    self.key_entered = 0

        self.last_widget = id

        if new_value > max:
            new_value = max
        elif new_value < min:
            new_value = min

        if new_value != value:
            return 1, new_value
        else:
            return 0, value

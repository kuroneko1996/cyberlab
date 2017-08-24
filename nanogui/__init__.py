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
        self.key_shift = False
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
            if self.active_item == 0 and self.mousedown == True:
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

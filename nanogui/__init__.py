class Nanogui:
    def __init__(self):
        self.mousex = 0
        self.mousey = 0
        self.mousedown = 0
        self.jdelay = 0
        self.hotitem = 0
        self.activeitem = 0

        # keyboard
        self.kbditem = 0
        self.keyentered = 0
        self.keyshift = 0
        self.lastwidget = 0

        self.draw_elements = []

    def draw(self):
        if len(self.draw_elements):
            return
        for k, v in enumerate(self.draw_elements):
            v()

    def pre(self, joystick):
        # called in update
        pass

    def after(self):
        # called in update
        pass
import settings
import pygame as pg
from settings import J_BUTTONS
import re


class Message:
    messages = []

    def __init__(self, text, picture=None):
        self.__text = text
        self.__text_typed = 0
        self.__picture = picture

        self.__init_graphics()

        Message.messages.append(self)

    def __init_graphics(self):
        self.text_box = pg.image.load(settings.TEXT_BOX).convert_alpha()
        self.font = pg.font.Font(*settings.FONT)
        self.font_smaller = pg.font.Font(*settings.FONT_SMALLER)

    def __str__(self):
        return self.__text[:self.__text_typed]

    def __repr__(self):
        if self.__picture:
            return "Message({0}, {1})".format(repr(self.__text), repr(self.__picture))
        else:
            return "Message({0})".format(repr(self.__text))

    def type_more(self):
        self.__text_typed = min(self.__text_typed + 1,
                                len(self.__text))

    def close(self):
        """
        Either finish typing this messages or switch to the next screen
        """
        self.__text_typed = len(self.__text)

    def __bool__(self):
        """
        A messages is true when it's complete
        :return: true if the messages is done typing
        """
        return len(self.__text) == self.__text_typed

    @property
    def picture(self):
        return self.__picture

    def render(self, display):
        """
        Renders self onto given display
        :param display: display on which to render the messages
        :return: nothing
        """
        self.__put_text_on_screen(display, str(self))

    def __put_text_on_screen(self, display, text):
        display.blit(self.text_box, (0, 360))

        line_num = 0
        for line in re.split("\n", text):
            if not is_a_line_comment(line):
                display.blit(self.font.render(line, True, (255, 255, 255)), (130, 380 + 20 * line_num))
                line_num += 1
        display.blit(self.font_smaller.render("[SPACE]", True, (255, 255, 255)), (560, 440))
        pg.display.flip()


def is_a_line_comment(message):
    return re.fullmatch("^#.*", message)

def update(game):
    """
    Handles user input regarding messages
    :return: nothing
    """
    if game.get_vbutton_jp('close') or game.get_joystick_jp(J_BUTTONS['A']) or game.get_joystick_jp(J_BUTTONS['B']):
        if Message.messages:
            if Message.messages[0]:
                Message.messages.pop(0)
            else:
                Message.messages[0].close()
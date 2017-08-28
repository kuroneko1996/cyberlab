import settings
import pygame as pg
from settings import J_BUTTONS, TYPING_SPEED
import re


def get_message(text, picture=None):
    if text and text[0] == "#":
        pass
    elif text and text[0] == "$":
        return ControlMessage(text, picture)
    else:
        return TextMessage(text, picture)


class Message:
    ICON_TEXT_BOX = None
    ICON_TEXT_BOX_TEXT_START_X = 130

    NARRATOR_TEXT_BOX = None
    NARRATOR_TEXT_BOX_TEXT_START_X = 20

    FONT = None
    FONT_SMALLER = None
    FONT_BIGGER = None

    messages = []
    text_box = None
    text_start_x = ICON_TEXT_BOX_TEXT_START_X

    def __init__(self):
        Message.messages.append(self)

        if not Message.ICON_TEXT_BOX:
            Message.ICON_TEXT_BOX = pg.image.load(settings.ICON_TEXT_BOX).convert_alpha()

        if not Message.NARRATOR_TEXT_BOX:
            Message.NARRATOR_TEXT_BOX = pg.image.load(settings.NARRATOR_TEXT_BOX).convert_alpha()

        if not Message.FONT:
            Message.FONT = pg.font.Font(*settings.FONT)

        if not Message.FONT_SMALLER:
            Message.FONT_SMALLER = pg.font.Font(*settings.FONT_SMALLER)

        if not Message.FONT_BIGGER:
            Message.FONT_BIGGER = pg.font.Font(*settings.FONT_BIGGER)

        if not Message.text_box:
            Message.text_box = Message.ICON_TEXT_BOX

    def __bool__(self):
        return False

    def update(self, game):
        pass

    def render(self, display):
        pass

    def close(self):
        pass


def update(game):
    """
    Handles user input regarding messages
    :return: nothing
    """
    if Message.messages:
        Message.messages[0].update(game)
        if Message.messages[0] and type(Message.messages[0]) == ControlMessage:
            Message.messages.pop(0)

    if (game.get_vbutton_jp('close') or
            game.get_joystick_jp(J_BUTTONS['A']) or
            game.get_joystick_jp(J_BUTTONS['B'])):
        if Message.messages:
            Message.messages[0].close()


class TextMessage(Message):
    """
    Text messages simply display text
    """
    def __init__(self, text, picture):
        super().__init__()

        self.__text = text
        self.__text_typed = 0
        self.__picture = picture

    def __str__(self):
        return self.__text[:self.__text_typed]

    def close(self):
        """
        Either finish typing this messages or switch to the next screen
        """

        if self:
            Message.messages.pop(0)
        else:
            self.__text_typed = len(self.__text)

    def __bool__(self):
        """
        A messages is true when it's complete
        :return: true if the messages is done typing
        """
        return len(self.__text) == self.__text_typed

    def update(self, game):
        if game.global_time % TYPING_SPEED < game.dt:
            self.__text_typed = min(self.__text_typed + 1,
                                    len(self.__text))

    def __put_text_on_screen(self, display):
        display.blit(self.text_box, (0, 360))

        line_num = 0
        for line in re.split("\n", self.__str__()):
            display.blit(self.FONT.render(line, True, (255, 255, 255)), (Message.text_start_x, 380 + 20 * line_num))
            line_num += 1
        display.blit(self.FONT_SMALLER.render("[SPACE]", True, (255, 255, 255)), (560, 440))
        pg.display.flip()

    def render(self, display):
        """
        Renders self onto given display
        :param display: display on which to render the messages
        :return: nothing
        """
        self.__put_text_on_screen(display)


class ControlMessage(Message):
    """
    Control messages can execute arbitrary code

    $style icon

    $style narrator

     ^-- change the messages style
    """
    def __init__(self, text, picture):
        super().__init__()

        self.__code = re.split(" ", text[1:])
        print(self.__code)

    def __bool__(self):
        # return true so that this could be
        # easily removed from the message queue
        return True

    def update(self, game):
        if self.__code[0] == "style":
            if self.__code[1] == "icon":
                Message.text_box = Message.ICON_TEXT_BOX
                Message.text_start_x = Message.ICON_TEXT_BOX_TEXT_START_X
            elif self.__code[1] == "narrator":
                Message.text_box = Message.NARRATOR_TEXT_BOX
                Message.text_start_x = Message.NARRATOR_TEXT_BOX_TEXT_START_X
            else:
                raise ValueError("Unexpected message style")

    def render(self, display):
        pass

    def close(self):
        Message.messages.remove(self)


def is_a_line_comment(line):
    """
    Returns true if given line is a comment
    :param line: line to be checked
    :return: true if the line is a comment, false otherwise
    """
    return re.fullmatch("^#.*", line)


def is_code(line):
    """
    Returns true if given line is a code
    :param line: line to be checked
    :return: true if the line is a code, false otherwise
    """
    return re.fullmatch("^\$.*", line)


def is_text(line):
    """
    Return true if given line is plain text
    :param line: line to be checked
    :return: true if the line is a text, false otherwise
    """
    return not (is_a_line_comment(line) or is_code(line))
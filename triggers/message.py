import settings
import pygame as pg
from settings import J_BUTTONS, TYPING_SPEED
import re
import collections


def get_message(text, picture=None):
    if text and text[0] == "#":
        pass
    elif text and text[0] == "$":
        return ControlMessage(text, picture)
    else:
        return TextMessage(text, picture)

MessageStyle = collections.namedtuple("MessageStyle", "frame text picture")
# frame is the position of the text box
# text is the position of the text
# picture is the picture of the text box


class Message:
    ICON_TEXT_BOX = None
    NARRATOR_TEXT_BOX = None
    BIG_TEXT_BOX = None

    FONT = None
    FONT_SMALLER = None
    FONT_BIGGER = None

    messages = []
    text_box = None
    speaker = "1"

    def __init__(self):

        if not Message.messages:
            Message.FONT = pg.font.Font(*settings.FONT)
            Message.FONT_SMALLER = pg.font.Font(*settings.FONT_SMALLER)
            Message.FONT_BIGGER = pg.font.Font(*settings.FONT_BIGGER)

            Message.ICON_TEXT_BOX = MessageStyle((0, 360),
                                                 (130, 370),
                                                 pg.image.load(settings.ICON_TEXT_BOX).convert_alpha())
            Message.NARRATOR_TEXT_BOX = MessageStyle((0, 360),
                                                     (20, 370),
                                                     pg.image.load(settings.NARRATOR_TEXT_BOX).convert_alpha())

            # TODO: move to the helper
            big_box_picture = pg.Surface((settings.SCREEN_WIDTH - 10,
                                          settings.SCREEN_HEIGHT - 10))
            big_box_picture.fill((24, 191, 60),
                               pg.Rect(2, 2,
                                       big_box_picture.get_width() - 4,
                                       big_box_picture.get_height() - 4))

            Message.BIG_TEXT_BOX = MessageStyle((5, 5),
                                             (10, 10),
                                             big_box_picture)

            Message.text_box = Message.ICON_TEXT_BOX

        Message.messages.append(self)

    @property
    def complete(self):
        return True

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
        if Message.messages[0].complete and type(Message.messages[0]) == ControlMessage:
            Message.messages.pop(0)

    if (game.get_vbutton_jp('next') or
            game.get_joystick_jp(J_BUTTONS['A'])):
        if Message.messages:
            Message.messages[0].close()
    if (game.get_vbutton_jp('close') or
            game.get_joystick_jp(J_BUTTONS['B'])):
        Message.messages = []


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

        if self.completed:
            Message.messages.pop(0)
        else:
            self.__text_typed = len(self.__text)

    @property
    def completed(self):
        """
        Returns true if message is complete
        :return: true if the messages is typed
        """
        return len(self.__text) == self.__text_typed

    def update(self, game):
        if game.global_time % TYPING_SPEED < game.dt:
            self.__text_typed = min(self.__text_typed + 1,
                                    len(self.__text))

    def __put_text_on_screen(self, display):
        display.blit(Message.text_box.picture, Message.text_box.frame)
        if Message.text_box == Message.ICON_TEXT_BOX:
            display.blit(pg.transform.scale(
                pg.image.load("assets/messages/avatars/{0}.png".format(Message.speaker))
                    .convert_alpha(),
                (105, 105)),
                (5, 367))

        line_num = 0
        for line in re.split("\n", self.__str__()):
            display.blit(self.FONT.render(line, True, (255, 255, 255)),
                         (Message.text_box.text[0],
                          Message.text_box.text[1] + 20 * line_num))
            line_num += 1
        display.blit(self.FONT_SMALLER.render("[RETURN]", True, (255, 255, 255)), (565, 455))
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

    def update(self, game):
        if self.__code[0] == "style":
            if self.__code[1] == "icon":
                Message.text_box = Message.ICON_TEXT_BOX
            elif self.__code[1] == "narrator":
                Message.text_box = Message.NARRATOR_TEXT_BOX
            elif self.__code[1] == "big":
                Message.text_box = Message.BIG_TEXT_BOX
            else:
                raise ValueError("Unexpected message style")

        if self.__code[0] == "speaker":
            Message.speaker = self.__code[1]

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
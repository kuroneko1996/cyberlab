import collections
from math import *

Message = collections.namedtuple("Message", "text switch_picture text_typed")


def make_message(text, switch_picture=False):
    """
    Makes a new message
    :param text: text
    :param switch_picture: if true, picture would be switched
    :return: message object
    """
    return Message(text, switch_picture, 0)


def type_message(message):
    """
    Type more parts of the message on the player's screen
    :param message: message to be typed
    :return: new message that's one or zero more characters longer
    """
    return Message(message.text,
                   message.switch_picture,
                   min(message.text_typed + 1,
                       len(message.text)))


def is_typed(message):
    """
    Return true if the message is completely typed
    :param message: message to be checked
    :return: true if the message is typed
    """
    return len(message.text) == message.text_typed


def finish_typing(message):
    """
    Finish typing the message
    :param message: message to finish typing
    :return: completely typed version of the message
    """
    return Message(message.text,
                   message.switch_picture,
                   len(message.text))
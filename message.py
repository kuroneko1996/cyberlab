import collections
from math import *


class Message:
    def __init__(self, text, picture=None):
        self.__text = text
        self.__text_typed = 0
        self.__picture = picture

    def __str__(self):
        return self.__text[:self.__text_typed]

    def type_more(self):
        self.__text_typed = min(self.__text_typed + 1,
                                len(self.__text))

    def finish_typing(self):
        self.__text_typed = len(self.__text)

    def is_typed(self):
        return len(self.__text) == self.__text_typed

    def has_picture(self):
        return self.__picture is not None

    def get_picture(self):
        return self.__picture
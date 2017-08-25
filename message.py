import collections

Message = collections.namedtuple("Message", "text switch_picture")


def make_message(text, switch_picture=False):
    """
    Makes a new message
    :param text: text
    :param switch_picture: if true, picture would be switched
    :return: message object
    """
    return Message(text, switch_picture)
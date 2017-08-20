# Threshold for the sign function
THRESHOLD = 0.000000001


def sgn(num):
    """
    Produce the sign of the number
    :param num: signed number
    :return: sign of the number
    """
    if num > THRESHOLD:
        return 1
    elif num < - THRESHOLD:
        return -1
    else:
        return 0
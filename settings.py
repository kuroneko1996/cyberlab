import pygame as pg

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WINDOW_TITLE = "Cyberpunk Laboratory"

FPS = 60

BG_COLOR = (0, 0, 0)

TILE_SIZE = 32
TYPING_SPEED = 0.05

MAX_LINE_LENGTH = 50
ICON_TEXT_BOX = "assets/messages/icon_text_box.png"
NARRATOR_TEXT_BOX = "assets/messages/narrator_text_box.png"
FONT_BIGGER = "assets/fonts/unifont-10.0.06.ttf", 32
FONT = "assets/fonts/unifont-10.0.06.ttf", 20
FONT_SMALLER = "assets/fonts/unifont-10.0.06.ttf", 14

SLITHER_SPEED = 0.05
FOV_RADIUS = 10
DEBUG_FOV = False
DARKEN_COLOR = (60, 60, 60)
LIGHT_COLOR = (40, 40, 10)

# change key mappings for keyboard
V_BUTTONS = {
    'left': [pg.K_LEFT, pg.K_a, pg.K_KP4],
    'right': [pg.K_RIGHT, pg.K_d, pg.K_KP6],
    'up': [pg.K_UP, pg.K_w, pg.K_KP8],
    'down': [pg.K_DOWN, pg.K_s, pg.K_KP2],
    # diagonal movement using numpad
    'top_left': [pg.K_KP7],
    'top_right': [pg.K_KP9],
    'bottom_left': [pg.K_KP1],
    'bottom_right': [pg.K_KP3],
    'pickup': [pg.K_e, pg.K_g, pg.K_KP5],
    'open_door': [pg.K_e, pg.K_RETURN, pg.K_KP5],
    'drop': [pg.K_q],
    'next': [pg.K_RETURN],
    'close': [pg.K_SPACE]
}
# end key mappings

JOYSTICK_THRESHOLD = 0.1
J_BUTTONS = {
    'A': 0,
    'B': 1,
    'X': 2,
    'Y': 3,
    'LB': 4,
    'RB': 5,
    'Back': 6,
    'Start': 7,
    'Guide': 8,
    'RStick': 9,
    'LStick': 10
}

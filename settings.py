# game options/settings
import pygame as pg
TITLE = "Jumpy!"
WIDTH = 480
HEIGHT = 600
FPS = 60

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
POW_SPAWN_PCT=85
BOOST_POWER=60

# Starting platforms
PLATFORM_LIST = [(225,HEIGHT - 40, WIDTH, 40),(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 335, 100, 20),
                 (350, 200, 100, 20),
                 (175, 100, 50, 20)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)

PLAYER_LAYER = 2
PLATFORM_LAYER = 1
MOB_LAYER = 2
POW_LAYER = 1
CLOUD_LAYER = 0

FONT_NAME='arial'
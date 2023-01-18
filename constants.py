import pygame
from win32api import GetSystemMetrics

pygame.init()

TILE_SIZE = 64
BLOCK_ID = (1, 2, 3, 4, 7, 8, 15, 16, 17, 18, 21, 22, 32, 33, 46, 47, 60, 61, 74, 75)
WATER_ID = (5, 19)
SPIKES_ID = (71,)
LAVA_ID = (6, 20)
STAIRS_ID = (57, 58)
CRYSTAL_ID = (36, 37, 38, 39, 50, 51, 52, 53)
FINISH_ID = (76, 90)
SAW_ID = (11, 12, 25, 26, 72)

GAME_TITLE = "pygameProject"

# SIZE = WIDTH, HEIGHT = 1300, 700
SIZE = WIDTH, HEIGHT = GetSystemMetrics(0)-20, GetSystemMetrics(1)-50

SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption(GAME_TITLE)

JUMP_POWER = 15
GRAVITY = 0.6

FPS = 75

HERO_SPEED = 6.9  # Скорость передвижения героя

ANIMATION_COOLDOWN = 100  # Частота обновления анимации

LEVEL_BACKGROUND_IMAGE = "background\\background_level_2.png"

MENU_BACKGROUND_IMAGE = "background\\background_menu.png"

FONT = pygame.font.SysFont("Roboto", 75)

TEXT_SIZE = 32

Title_COLOR = pygame.Color((34, 139, 34))

TextButton_TEXT_COLOR = pygame.Color((0, 102, 204))
TextButton_TEXT_COLOR_MOUSE_MOTION = pygame.Color((51, 153, 255))

LevelButton_BACGROUND_COLOR = pygame.Color((0, 102, 204, 128))
LevelButton_BACGROUND_COLOR_MOUSE_MOTION = pygame.Color((51, 153, 255, 128))

SAW_ROTATION_ANGLE = 10

SAW_DAMAGE = 0.75
SPIKES_DAMAGE = 0.5
LAVA_DAMAGE = 1
WATER_DAMAGE = 1

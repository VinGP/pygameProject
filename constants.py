import pygame

pygame.init()

TILE_SIZE = 64
BLOCK_ID = (1, 2, 3, 4, 7, 8, 15, 16, 17, 18, 21, 22, 32, 33, 46, 47, 60, 61, 74, 75)
WATER_ID = (5, 19)
SPIKES_ID = (71,)
LAVA_ID = (6, 20)
STAIRS_ID = (57, 58)
CRYSTAL_ID = (36, 37, 38, 39, 50, 51, 52, 53)
FINISH_ID = (76, 90)

GAME_TITLE = "pygameProject"

SIZE = WIDTH, HEIGHT = 1300, 700
SCREEN = pygame.display.set_mode(SIZE)
pygame.display.set_caption(GAME_TITLE)

JUMP_POWER = 15
GRAVITY = 0.6

FPS = 77

HERO_SPEED = 7  # Скорость передвижения героя

ANIMATION_COOLDOWN = 100  # Частота обновления анимации

LEVEL_BACKGROUND_IMAGE = "background\\background_level_2.png"

MENU_BACKGROUND_IMAGE = "background\\background_menu.png"

FONT = pygame.font.SysFont("Roboto", 100)

TEXT_SIZE = 32

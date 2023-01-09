import pygame


def play_music():
    bg_sound = pygame.mixer.Sound('data/sounds/bird.mp3')
    bg_sound.play(-1)


def sound_spike():
    pygame.mixer.music.load('data/sounds/spike.mp3')
    pygame.mixer.music.play(0)


def sound_lava():
    pygame.mixer.music.load('data/sounds/lava.mp3')
    pygame.mixer.music.play(0)


def sound_crystal():
    pygame.mixer.music.load('data/sounds/crystal.mp3')
    pygame.mixer.music.play(0)


def sound_finish():
    pygame.mixer.music.load('data/sounds/finish.mp3')
    pygame.mixer.music.play(0)


def sound_stairs(times):
    pygame.mixer.music.load('data/sounds/stairs.mp3')
    pygame.mixer.music.play(times)


def sound_water():
    pygame.mixer.music.load('data/sounds/water.mp3')
    pygame.mixer.music.play(0)


def sound_ground(times):
    ground_sound = pygame.mixer.Sound('data/sounds/ground.mp3')
    ground_sound.play(times)

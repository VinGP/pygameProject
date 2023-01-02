import os

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Не удаётся загрузить:", name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class T(pygame.sprite.Sprite):
    """Класс для отслеживания точки (0,0) уровня.
    Необходим для правильного позиционирования камеры"""

    def __init__(self, x, y, all_sprites):
        super().__init__(all_sprites)
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(x, y, 0, 0)

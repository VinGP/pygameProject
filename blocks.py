import pygame


class AbstractSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, sprite_groups: list[pygame.sprite.Group]):
        super().__init__(*sprite_groups)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hit_box = self.rect.copy()
        # у каждого наследника должен быть
        # этот атрибут. По его значению будут вычисляться коллизии

    def update(self):
        self.hit_box.midbottom = self.rect.midbottom


class Block(AbstractSprite):
    """Блок"""

    def __init__(self, x, y, img, sprite_groups: list[pygame.sprite.Group]):
        super().__init__(img, x, y, sprite_groups)


class Water(AbstractSprite):
    """Вода"""

    def __init__(self, x, y, img, sprite_groups):
        super().__init__(img, x, y, sprite_groups)


class Lava(AbstractSprite):
    """Лава"""

    def __init__(self, x, y, img, sprite_groups):
        super().__init__(img, x, y, sprite_groups)


class Spikes(AbstractSprite):
    """Шипы"""

    def __init__(self, x, y, img, sprite_groups):
        super().__init__(img, x, y, sprite_groups)
        self.hit_box = pygame.Rect(
            0,
            0 + self.image.get_height() // 2,
            self.image.get_width(),
            self.image.get_height() // 2,
        )
        self.hit_box.bottom = self.rect.bottom


class Stairs(AbstractSprite):
    """Лестница"""

    def __init__(self, img, x, y, sprite_groups):
        super().__init__(img, x, y, sprite_groups)

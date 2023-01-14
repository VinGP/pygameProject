import pygame.transform

from constants import *


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
        self.damage = WATER_DAMAGE


class Lava(AbstractSprite):
    """Лава"""

    def __init__(self, x, y, img, sprite_groups):
        super().__init__(img, x, y, sprite_groups)
        self.damage = LAVA_DAMAGE


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
        self.damage = SPIKES_DAMAGE


class Stairs(AbstractSprite):
    """Лестница"""

    def __init__(self, img, x, y, sprite_groups):
        super().__init__(img, x, y, sprite_groups)


class Finish(AbstractSprite):
    def __init__(self, image, x, y, sprite_groups: list[pygame.sprite.Group]):
        super().__init__(image, x, y, sprite_groups)
        self.hit_box = self.rect.inflate(-40, -40)

    def update(self):
        self.hit_box.center = self.rect.center


class Saw(AbstractSprite):
    def __init__(
            self,
            image,
            x,
            y,
            sprite_groups: list[pygame.sprite.Group],
            animation_cooldown=ANIMATION_COOLDOWN,
            rotation_angle=SAW_ROTATION_ANGLE,
    ):
        self.orig_img = image
        super().__init__(image, x, y, sprite_groups)
        self.hit_box = self.rect.inflate(-8, -8)
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = animation_cooldown
        self.rotation_angle = rotation_angle
        self.angle = 0
        self.damage = SAW_DAMAGE

    @staticmethod
    def rotate(image, rect, angle):
        """Rotate the image while keeping its center."""
        # Rotate the original image without modifying it.
        new_image = pygame.transform.rotate(image, angle)
        # Get a new rect with the center of the old rect.
        rect = new_image.get_rect(center=rect.center)
        return new_image, rect

    def update(self):
        self.update_animation()
        self.hit_box.center = self.rect.center
        # self.draw()

    def draw(self):
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hit_box, 2)
        pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)

    def update_animation(self):
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.angle += self.rotation_angle
            self.image, self.rect = self.rotate(self.orig_img, self.rect, self.angle)
            self.angle %= 360

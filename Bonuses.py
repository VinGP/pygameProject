import pygame

crystal_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


class AbstractBonus(pygame.sprite.Sprite):
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


class Crystal(AbstractBonus):
    def __init__(self, image, x, y):
        super().__init__(image, x, y, [all_sprites, crystal_group])
        self.hit_box = self.rect.inflate(-15, -15)

    def update(self):
        self.hit_box.center = self.rect.center

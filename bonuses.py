from constants import *


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
    def __init__(self, img, x, y, sprite_groups):
        super().__init__(img, x, y, sprite_groups)
        self.hit_box = self.rect.inflate(-15, -15)

    def update(self):
        self.hit_box.center = self.rect.center


class CrystalCounter:
    def __init__(self, x, y, count_crystals, crystal_image):
        self.count_crystals = count_crystals
        self.collected_crystals = 0
        self.image = crystal_image
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, int(TILE_SIZE * 0.8))

    def collect_crystal(self):
        self.collected_crystals += 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        text = self.font.render(
            f"{self.collected_crystals}/{self.count_crystals}",
            True,
            pygame.color.Color("black"),
        )
        text_x = self.x + self.image.get_width()
        text_y = self.y + (self.image.get_height() - text.get_height()) // 2
        screen.blit(text, (text_x, text_y))

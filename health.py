from constants import *
from tools import load_image


class Health:
    """
    Класс для отображения здоровья
    """

    def __init__(self, health):
        self.health = health
        self.full_health_img = load_image(rf"health\0.png")
        self.half_health_img = load_image(rf"health\2.png")

    def draw(self, screen):
        for i in range(int(self.health)):
            screen.blit(self.full_health_img, (TILE_SIZE * i, 0))
        if int(self.health * 10 % 10) != 0:
            screen.blit(
                self.half_health_img, (TILE_SIZE * int(self.health * 10 // 10), 0)
            )

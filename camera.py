from constants import *


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, t, level_width, level_height):
        self.level_height = level_height
        self.level_width = level_width
        self.dx = 0
        self.dy = 0
        self.t = t

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):

        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
        if self.t.rect.x + self.dx > 0:
            self.dx = -1 * self.t.rect.x
        elif abs(self.t.rect.x + self.dx) + WIDTH > self.level_width:
            self.dx = abs(self.t.rect.x) + WIDTH - self.level_width
        if abs(self.t.rect.y + self.dy) + HEIGHT > self.level_height - 1:
            self.dy = abs(self.t.rect.y) + HEIGHT - self.level_height
        elif self.t.rect.y + self.dy > 0:
            self.dy = -self.t.rect.y

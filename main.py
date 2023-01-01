import time

import pygame
import os
import pytmx
from constants import *
from abc import ABC

pygame.init()
pygame.display.set_caption("Название")
screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

block_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
water_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()


class Abstract_Item(pygame.sprite.Sprite, ABC):
    def __init__(self, image, x, y, *sprite_group):
        super().__init__(*sprite_group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    @property
    def hit_box(self):
        pass

    @hit_box.setter
    def hit_box(self, val):
        pass

    @hit_box.getter
    def hit_box(self):
        return None


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


class Level:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(filename)

        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.load_level()

    def load_level(self):
        for x in range(self.width):
            for y in range(self.height):
                n = self.map.get_tile_gid(x, y, 0)
                if n != 0:
                    id = self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)]
                    img = self.map.get_tile_image(x, y, 0)
                    if id in BLOCK_ID:
                        Block(x=x * TILE_SIZE, y=y * TILE_SIZE, img=img)
                    elif id in WATER_ID:
                        Water(x=x * TILE_SIZE, y=y * TILE_SIZE, img=img)
                    elif id in SPIKES_ID:
                        Spikes(x=x * TILE_SIZE, y=y * TILE_SIZE, img=img)
                    elif id in LAVA_ID:
                        Lava(x=x * TILE_SIZE, y=y * TILE_SIZE, img=img)
                    elif id in STAIRS_ID:
                        Stairs(x=x * TILE_SIZE, y=y * TILE_SIZE, img=img)

    def render(self, screen):
        for y in range(self.width):
            for x in range(self.height):
                try:
                    image = self.map.get_tile_image(x, y, 0)
                except Exception:
                    continue
                if image is not None:
                    screen.blit(image, (self.tile_size * x, self.tile_size * y))


class Hero(pygame.sprite.Sprite):
    """Главного героя игры"""

    def __init__(self, animation_pictures_folder, x, y, speed=5, animation_cooldown=100):
        super().__init__(all_sprites)
        self.frames = []
        self.animation_pictures_folder = animation_pictures_folder
        self.gravity = GRAVITY

        self.jump = False
        self.moving_left = False
        self.moving_right = False

        self.animation_cooldown = animation_cooldown  # Частота обновления анимации

        self.speed = speed

        self.xvel = 0
        self.yvel = 0

        self.onGround = False

        self.animation_list = []
        self.cur_frame = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        """
        Action:
        0 - idle
        1 - climb
        2 - jump
        3 - walk
        """

        self.load_animation()
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.hit_box = pygame.Rect(0, 0, self.image.get_width() - 16, self.image.get_height() - 30)
        self.hit_box.bottom = self.rect.bottom

    def load_animation(self):
        animation_types = ["idle", "climb", "jump", "walk"]
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f"data/{self.animation_pictures_folder}/{animation}"))
            for i in range(num_of_frames):
                img = load_image(f"{self.animation_pictures_folder}\{animation}\{animation}{i}.png")
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.cur_frame]

    def update(self):
        self.move()
        self.update_action()
        self.update_animation()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hit_box, 2)
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 2)

    def move(self):
        if not self.moving_left and not self.moving_right:
            self.xvel = 0
        if self.moving_left:
            self.xvel = -self.speed

        if self.moving_right:
            self.xvel = self.speed

        if not self.onGround:
            self.yvel += self.gravity
        if self.jump:
            if self.onGround:
                self.yvel = -JUMP_POWER

        self.rect.x += self.xvel
        self.hit_box.midbottom = self.rect.midbottom

        self.collide(self.xvel, 0)

        self.rect.y += self.yvel
        self.hit_box.y += self.yvel
        self.rect.midbottom = self.hit_box.midbottom
        self.collide(0, self.yvel)
        self.rect.midbottom = self.hit_box.midbottom

    def collide(self, xvel, yvel):
        self.onGround = False

        for block in block_group:
            if self.hit_box.colliderect(block.rect):
                if xvel > 0:
                    self.hit_box.right = block.rect.left
                if xvel < 0:
                    self.hit_box.left = block.rect.right
                if yvel > 0:
                    self.hit_box.bottom = block.rect.top
                    self.onGround = True
                    self.yvel = 1
                if yvel < 0:
                    self.hit_box.top = block.rect.bottom
                    self.yvel = 0

    def update_action(self):
        if not self.onGround:
            new_action = 2
        elif self.moving_right or self.moving_left:
            new_action = 3
        else:
            new_action = 0
        if new_action != self.action:
            self.action = new_action
            self.cur_frame = 0

    def update_animation(self):
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.image = self.animation_list[self.action][self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.animation_list[self.action])

            if self.moving_left:
                self.image = pygame.transform.flip(self.image, True, False)


class Block(pygame.sprite.Sprite):
    """Блок"""

    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self, all_sprites, block_group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Health:
    """
    Класс для отображения здоровья
    """


class Water(pygame.sprite.Sprite):
    """Вода"""

    def __init__(self, img, x, y):
        super().__init__(all_sprites, water_group)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Lava(pygame.sprite.Sprite):
    """Лава"""

    def __init__(self, img, x, y):
        super().__init__(all_sprites, lava_group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Spikes(pygame.sprite.Sprite):
    """Шипы"""

    def __init__(self, img, x, y):
        super().__init__(all_sprites, spikes_group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Stairs(pygame.sprite.Sprite):
    """Лестница"""

    def __init__(self, img, x, y):
        super().__init__(all_sprites, stairs_group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, t):
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
        elif abs(self.t.rect.x + self.dx) + WIDTH > level_width:
            self.dx = abs(self.t.rect.x) + WIDTH - level_width

        if abs(self.t.rect.y + self.dy) + HEIGHT > level_height - 1:
            self.dy = abs(self.t.rect.y) + HEIGHT - level_height
        elif self.t.rect.y + self.dy > 0:
            self.dy = -self.t.rect.y


class T(pygame.sprite.Sprite):
    """Класс для отслеживания точки (0,0) уровня.
    Необходим для правильного позиционирования камеры"""

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(x, y, 0, 0)


level = Level(filename="data/map.tmx")
hero = Hero(
    "hero",
    TILE_SIZE,
    (level.height - 3) * TILE_SIZE - TILE_SIZE,
    speed=HERO_SPEED,
    animation_cooldown=ANIMATION_COOLDOWN,
)

level_height = level.map.height * TILE_SIZE
level_width = level.map.width * TILE_SIZE

camera = Camera(T(0, 0))

if __name__ == "__main__":

    screen.fill((0, 0, 0))
    running = True

    while running:
        screen.fill((0, 0, 0))
        # screen.fill(pygame.Color("blue"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    hero.moving_left = True
                if event.key == pygame.K_d:
                    hero.moving_right = True

                if event.key == pygame.K_w and hero.alive:
                    hero.jump = True
                if event.key == pygame.K_ESCAPE:
                    run = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    hero.moving_left = False
                if event.key == pygame.K_d:
                    hero.moving_right = False
                if event.key == pygame.K_w:
                    hero.jump = False

        # изменяем ракурс камеры
        camera.update(hero)
        # # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        all_sprites.update()

        hero.draw(screen)
        print(clock.get_fps())
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()

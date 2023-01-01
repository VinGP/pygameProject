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


class AbstractSprite(pygame.sprite.Sprite, ABC):
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

    def __init__(
            self, animation_pictures_folder, x, y, speed=5, animation_cooldown=100
    ):
        super().__init__(all_sprites)
        self.animation_pictures_folder = animation_pictures_folder
        self.gravity = GRAVITY

        self.moving_left = False
        self.moving_right = False

        self.moving_up = False
        self.moving_down = False

        self.on_stairs = False  # герой на лестнице

        self.animation_cooldown = animation_cooldown  # Частота обновления анимации

        self.speed = speed

        self.xvel = 0
        self.yvel = 0

        self.onGround = False

        self.t = T(x, y)

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
        self.image = self.animation_list[self.action][self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.hit_box = pygame.Rect(
            0, 0, self.image.get_width() - 18, self.image.get_height() - 30
        )
        self.hit_box.bottom = self.rect.bottom

    def load_animation(self):
        animation_types = ["idle", "climb", "jump", "walk"]
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(
                os.listdir(f"data/{self.animation_pictures_folder}/{animation}")
            )
            for i in range(num_of_frames):
                img = load_image(
                    f"{self.animation_pictures_folder}\{animation}\{animation}{i}.png"
                )
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def update(self):

        self.move()
        self.update_action()
        self.update_animation()

        self.hit_box.midbottom = self.rect.midbottom

        # self.draw(screen)

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

        if not self.onGround and not self.on_stairs:
            self.yvel += self.gravity
        if self.moving_up:
            if self.onGround:
                self.yvel = -JUMP_POWER
        if self.on_stairs:
            if self.moving_up:
                self.yvel = -self.speed
            elif self.moving_down:
                self.yvel = self.speed
            else:
                self.yvel = 0

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
        self.on_stairs = False

        for block in block_group:
            if self.hit_box.colliderect(block.hit_box):
                if xvel > 0:
                    self.hit_box.right = block.hit_box.left
                if xvel < 0:
                    self.hit_box.left = block.hit_box.right
                if yvel > 0:
                    self.hit_box.bottom = block.hit_box.top
                    self.onGround = True
                    self.yvel = 1
                if yvel < 0:
                    self.hit_box.top = block.hit_box.bottom
                    self.yvel = 0
        for water in water_group:
            if self.hit_box.colliderect(water.hit_box):
                self.rect.move_ip(
                    -(self.rect.x - self.t.rect.x), -(self.rect.y - self.t.rect.y)
                )
                self.hit_box.midbottom = self.rect.midbottom

        for lava in lava_group:
            if self.hit_box.colliderect(lava.hit_box):
                self.rect.move_ip(
                    -(self.rect.x - self.t.rect.x), -(self.rect.y - self.t.rect.y)
                )
                self.hit_box.midbottom = self.rect.midbottom

        for spikes in spikes_group:
            if self.hit_box.colliderect(spikes.hit_box):
                print("spikes")

        for stairs in stairs_group:
            if self.hit_box.colliderect(stairs.hit_box):
                self.on_stairs = True
                self.onGround = False

    def update_action(self):
        if not self.onGround and not self.on_stairs:
            new_action = 2
        elif self.on_stairs:
            new_action = 1
        elif self.moving_right or self.moving_left:
            new_action = 3
        else:
            new_action = 0
        if new_action != self.action:
            self.action = new_action
            self.cur_frame = 0

    def update_animation(self):
        if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
            if self.on_stairs:
                self.image = self.animation_list[self.action][self.cur_frame]
                if (
                        self.moving_down
                        or self.moving_up
                        and pygame.time.get_ticks() - self.update_time
                        > self.animation_cooldown * 2
                ):
                    self.update_time = pygame.time.get_ticks()
                    self.cur_frame = (self.cur_frame + 1) % len(
                        self.animation_list[self.action]
                    )
            else:
                self.image = self.animation_list[self.action][self.cur_frame]
                self.update_time = pygame.time.get_ticks()
                self.cur_frame = (self.cur_frame + 1) % len(
                    self.animation_list[self.action]
                )

            if self.moving_left:
                self.image = pygame.transform.flip(self.image, True, False)


class Block(AbstractSprite):
    """Блок"""

    def __init__(self, x, y, img):
        super().__init__(img, x, y, [all_sprites, block_group])


class Health:
    """
    Класс для отображения здоровья
    """


class Water(AbstractSprite):
    """Вода"""

    def __init__(self, x, y, img):
        super().__init__(img, x, y, [all_sprites, water_group])


class Lava(AbstractSprite):
    """Лава"""

    def __init__(self, x, y, img):
        super().__init__(img, x, y, [all_sprites, lava_group])


class Spikes(AbstractSprite):
    """Шипы"""

    def __init__(self, x, y, img):
        super().__init__(img, x, y, [all_sprites, spikes_group])
        self.hit_box = pygame.Rect(
            0,
            0 + self.image.get_height() // 2,
            self.image.get_width(),
            self.image.get_height() // 2,
        )
        self.hit_box.bottom = self.rect.bottom

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hit_box, 2)
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)


class Stairs(AbstractSprite):
    """Лестница"""

    def __init__(self, img, x, y):
        super().__init__(img, x, y, [all_sprites, stairs_group])


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
                if event.key == pygame.K_w:
                    hero.moving_up = True
                if event.key == pygame.K_s:
                    hero.moving_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    hero.moving_left = False
                if event.key == pygame.K_d:
                    hero.moving_right = False
                if event.key == pygame.K_w:
                    hero.moving_up = False
                if event.key == pygame.K_s:
                    hero.moving_down = False

        # изменяем ракурс камеры
        camera.update(hero)
        # # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        all_sprites.draw(screen)
        all_sprites.update()

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()

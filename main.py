import pygame
import os
import pytmx

TILE_SIZE = 64
BLOCK_ID = (1, 2, 3, 4, 7, 8, 15, 16, 17, 18, 21, 22, 32, 33, 46, 47, 60, 61, 74, 75)
WATER_ID = (5, 19)
SPIKES_ID = (71,)
LAVA_ID = (6, 20)
STAIRS_ID = (57, 58)
JUMP_POWER = 15

block_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
water_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
stairs_group = pygame.sprite.Group()


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
        print(self.map.images)

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
    def __init__(self, sheet, columns, rows, x, y, speed=5):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.gravity = GRAVITY

        self.jump = False
        self.moving_left = False
        self.moving_right = False

        self.sprite_update_time = 100

        self.speed = speed

        self.xvel = 0
        self.yvel = 0

        self.onGround = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(
            0, 0, sheet.get_width() // columns, sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                )

    def update(self):
        self.move()
        # self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        # self.image = self.frames[self.cur_frame]

    def move(self):
        # print(self.yvel, self.onGround, self.rect.y)
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

        self.onGround = False

        self.rect.x += self.xvel
        self.collide(self.xvel, 0)
        self.rect.y += self.yvel
        self.collide(0, self.yvel)

    def collide(self, xvel, yvel):
        for block in block_group:
            if pygame.sprite.collide_rect(self, block):
                if xvel > 0:
                    self.rect.right = block.rect.left
                if xvel < 0:
                    self.rect.left = block.rect.right
                if yvel > 0:
                    self.rect.bottom = block.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = block.rect.bottom
                    self.yvel = 0


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self, all_sprites, block_group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Health:
    """
    Класс для отображения здоровь
    """


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__(all_sprites, water_group)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Lava(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__(all_sprites, water_group)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)


class Spikes(pygame.sprite.Sprite):
    """Шипы"""

    def __init__(self, img, x, y):
        super().__init__(all_sprites, water_group)

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
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


pygame.init()
pygame.display.set_caption("Название")
size = width, height = 900, 500
# size = width, height = 2000, 2000

screen = pygame.display.set_mode(size)

camera = Camera()

GRAVITY = 0.6

fps = 60

clock = pygame.time.Clock()
level = Level(filename="data/map.tmx")
# hero = Hero(load_image("hero_tiles.png"), 4, 2, level.width // 2 * TILE_SIZE, level.height * TILE_SIZE - TILE_SIZE)
hero = Hero(
    load_image("hero.png"),
    1,
    1,
    TILE_SIZE,
    (level.height - 3) * TILE_SIZE - TILE_SIZE,
    speed=7
)

if __name__ == "__main__":

    screen.fill((0, 0, 0))
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    hero.moving_left = True
                if event.key == pygame.K_d:
                    hero.moving_right = True

                if event.key == pygame.K_w and hero.alive:
                    hero.jump = True
                if event.key == pygame.K_ESCAPE:
                    run = False

            # keyboard button released
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
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()



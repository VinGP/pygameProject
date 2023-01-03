from camera import Camera
import pytmx
from blocks import *
from bonuses import *
from hero import Hero
from state import LevelState
from tools import load_image, T
from constants import *


class Level:
    def __init__(self, level_id, level_map_file_path):
        self.level_id = level_id
        self.map = pytmx.load_pygame(level_map_file_path)
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth

        self.all_sprites = pygame.sprite.Group()
        self.block_group = pygame.sprite.Group()
        self.water_group = pygame.sprite.Group()
        self.spikes_group = pygame.sprite.Group()
        self.stairs_group = pygame.sprite.Group()
        self.lava_group = pygame.sprite.Group()
        self.crystal_group = pygame.sprite.Group()
        self.finish_group = pygame.sprite.Group()

        self.crystal_counter = None

        self.crystal_counter_img = load_image(r"Bonuses\Crystal\0.png")

        self.load_level()

        self.crystal_counter = CrystalCounter(
            0, TILE_SIZE // 2, 16, self.crystal_counter_img
        )

        self.hero = Hero(
            level=self,
            animation_pictures_folder="hero",
            x=TILE_SIZE,
            y=(self.height - 3) * TILE_SIZE - TILE_SIZE,
            speed=HERO_SPEED,
            animation_cooldown=ANIMATION_COOLDOWN,
        )
        t = T(0, 0, self.all_sprites)
        self.camera = Camera(t, self.width * TILE_SIZE, self.height * TILE_SIZE)
        self.background = pygame.transform.scale(
            load_image(LEVEL_BACKGROUND_IMAGE), (WIDTH, HEIGHT)
        )
        self.state = LevelState.Run

    def load_level(self):
        for x in range(self.width):
            for y in range(self.height):
                n = self.map.get_tile_gid(x, y, 0)
                if n != 0:
                    id = self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)]
                    img = self.map.get_tile_image(x, y, 0)
                    if id in BLOCK_ID:
                        Block(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            img=img,
                            sprite_groups=[self.all_sprites, self.block_group],
                        )
                    elif id in WATER_ID:
                        Water(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            img=img,
                            sprite_groups=[self.all_sprites, self.water_group],
                        )
                    elif id in SPIKES_ID:
                        Spikes(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            img=img,
                            sprite_groups=[self.all_sprites, self.spikes_group],
                        )
                    elif id in LAVA_ID:
                        Lava(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            img=img,
                            sprite_groups=[self.all_sprites, self.lava_group],
                        )
                    elif id in STAIRS_ID:
                        Stairs(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            img=img,
                            sprite_groups=[self.all_sprites, self.stairs_group],
                        )
                    elif id in CRYSTAL_ID:
                        self.crystal_counter_img = img
                        Crystal(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            img=img,
                            sprite_groups=[self.all_sprites, self.crystal_group],
                        )
                    elif id in FINISH_ID:
                        Finish(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            image=img,
                            sprite_groups=[self.all_sprites, self.finish_group],
                        )

    def check_state(self):
        if not self.hero.is_alive():
            self.state = LevelState.Lose

    def get_state(self):
        return self.state

    def render(self, events):
        SCREEN.blit(self.background, (0, 0))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.hero.moving_left = True
                if event.key == pygame.K_d:
                    self.hero.moving_right = True
                if event.key == pygame.K_w:
                    self.hero.moving_up = True
                if event.key == pygame.K_s:
                    self.hero.moving_down = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.hero.moving_left = False
                if event.key == pygame.K_d:
                    self.hero.moving_right = False
                if event.key == pygame.K_w:
                    self.hero.moving_up = False
                if event.key == pygame.K_s:
                    self.hero.moving_down = False

        # изменяем ракурс камеры
        self.camera.update(self.hero)
        # обновляем положение всех спрайтов
        for sprite in self.all_sprites:
            self.camera.apply(sprite)
        self.all_sprites.draw(SCREEN)
        self.all_sprites.update()
        self.hero.health.draw(SCREEN)
        self.crystal_counter.draw(screen=SCREEN)
        self.check_state()

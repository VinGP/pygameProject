from constants import *
from health import Health
import os

from state import LevelState
from tools import load_image, T


class Hero(pygame.sprite.Sprite):
    """Главного героя игры"""

    def __init__(
        self, level, animation_pictures_folder, x, y, speed=5, animation_cooldown=100
    ):
        self.level = level

        super().__init__(self.level.all_sprites)
        self.animation_pictures_folder = animation_pictures_folder
        self.gravity = GRAVITY

        self.health = Health(3)

        self.moving_left = False
        self.moving_right = False

        self.moving_up = False
        self.moving_down = False

        self.spike_jump = False  # Прыжок от шипов

        self.on_stairs = False  # герой на лестнице

        self.animation_cooldown = animation_cooldown  # Частота обновления анимации

        self.speed = speed

        self.xvel = 0
        self.yvel = 0

        self.onGround = False

        self.t = T(x, y, level.all_sprites)

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
                    f"{self.animation_pictures_folder}\\{animation}\\{animation}{i}.png"
                )
                temp_list.append(img)
            self.animation_list.append(temp_list)

    def is_alive(self):
        return self.health.health > 0

    def update(self):

        self.move()
        self.update_action()
        self.update_animation()

        self.hit_box.midbottom = self.rect.midbottom

        # self.draw()

    def draw(self):
        pygame.draw.rect(SCREEN, (255, 0, 0), self.hit_box, 2)
        pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)
        pygame.draw.rect(SCREEN, (0, 0, 255), self.rect, 2)

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
        if self.spike_jump:
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

        for block in self.level.block_group:
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
        for water in self.level.water_group:
            if self.hit_box.colliderect(water.hit_box):
                self.rect.move_ip(
                    -(self.rect.x - self.t.rect.x), -(self.rect.y - self.t.rect.y)
                )
                self.hit_box.midbottom = self.rect.midbottom
                self.health.health -= 1

        for lava in self.level.lava_group:
            if self.hit_box.colliderect(lava.hit_box):
                self.rect.move_ip(
                    -(self.rect.x - self.t.rect.x), -(self.rect.y - self.t.rect.y)
                )
                self.hit_box.midbottom = self.rect.midbottom
                self.health.health -= 1

        for spikes in self.level.spikes_group:
            if self.hit_box.colliderect(spikes.hit_box):
                if self.spike_jump:
                    break
                self.spike_jump = True
                self.health.health -= 0.5
                break
        else:
            self.spike_jump = False

        for stairs in self.level.stairs_group:
            if self.hit_box.colliderect(stairs.hit_box):
                self.on_stairs = True
                self.onGround = False

        for crystal in self.level.crystal_group:
            if self.hit_box.colliderect(crystal.hit_box):
                self.level.crystal_counter.collect_crystal()
                crystal.kill()

        for finish in self.level.finish_group:
            if self.hit_box.colliderect(finish.hit_box):
                self.level.state = LevelState.Win

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

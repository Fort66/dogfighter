import pygame as pg

from pygame.transform import scale_by, rotozoom
from pygame.image import load

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_c, K_k

from pygame.sprite import Sprite, Group, groupcollide
from pygame.math import Vector2

from icecream import ic

from time import time

# pg.init()

from ..groups.class_AllSprites import all_sprites
from .class_PlayerShoot import PlayerShoot
from .class_Explosions import Explosions
from ..screens.class_Screen import win
from ..groups.class_SpritesGroups import groups
from ..logic.class_Signals import signals

from classes.screens.class_GameOverScreen import game_over_screen

# player_group = Group()
# player_rockets_group = Group()
# explosion_group = Group()


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = scale_by(load("images/su-33.png").convert_alpha(), 0.15)
        # self.image.fill('SteelBlue')
        self.image_rotation = self.image
        self.rect = self.image.get_rect(
            center=(win.screen.get_width() // 2, win.screen.get_height() // 2)
        )
        self.speed = 5
        self._layer = 2
        self.shoot_time = 1
        self.permission_shoot = 1
        self.direction_x = 0
        groups.player_group.add(self)
        all_sprites.add(self)

    def move(self):
        keys = pg.key.get_pressed()
        if True in keys:
            if keys[K_UP] or keys[K_w]:
                self.rect.move_ip(0, -self.speed) if self.rect.top > 0 else None
                self.image_rotation = self.image
                self.image_rotation = rotozoom(self.image_rotation, 30, 1)
                self.rect = self.image_rotation.get_rect(center=self.rect.center)

            if keys[K_DOWN] or keys[K_s]:
                (
                    self.rect.move_ip(0, self.speed)
                    if self.rect.bottom < win.screen.get_height()
                    else None
                )
                self.image_rotation = self.image
                self.image_rotation = rotozoom(self.image_rotation, -30, 1)
                self.rect = self.image_rotation.get_rect(center=self.rect.center)

            if keys[K_LEFT] or keys[K_a]:
                self.rect.move_ip(-self.speed, 0) if self.rect.left > 0 else None
                self.direction_x = -1

            if keys[K_RIGHT] or keys[K_d]:
                (
                    self.rect.move_ip(self.speed, 0)
                    if self.rect.right < win.screen.get_width()
                    else None
                )
                self.direction_x = 1

            if keys[K_k]:
                self.image_rotation = self.image
                self.image_rotation = rotozoom(self.image_rotation, 60, 1)
                self.speed = -3
                self.rect = self.image_rotation.get_rect(center=self.rect.center)

            if keys[K_c]:
                if not self.shoot_time:
                    self.shoot_time = time()
                if time() - self.shoot_time >= self.permission_shoot:
                    shoot = PlayerShoot(
                        pos=(self.rect.centerx - 46, self.rect.centery + 15),
                        speed=self.speed * 2,
                    )
                    groups.player_rockets_group.add(shoot)
                    all_sprites.add(shoot)
                    self.shoot_time = time()

        else:
            self.image_rotation = self.image
            self.image_rotation = rotozoom(self.image_rotation, 0, 1)
            self.speed = 5
            self.rect = self.image_rotation.get_rect(center=self.rect.center)



    def collisions(self):
        rocket_collide = groupcollide(groups.rockets_group, groups.player_rockets_group, True, True)
        if rocket_collide:
            hits = list(rocket_collide.keys())[0]
            self.explosion_rocket = Explosions(hits.rect.center, 1)
            self.explosion_rocket.speed = hits.speed * hits.direction_x

        player_collide = groupcollide(groups.player_group, groups.rockets_group, True, True)

        if player_collide:
            signals.change_signals('game_over')
        #     self.explosion_player = Explosions(win.screen, self.rect.center, 2)
        #     self.explosion_player.speed = self.speed * self.direction_x
            # if self.explosion_player.image._ended:
            #     player_collide.clear()
            #     all_sprites.remove(self)

    def update(self):
        self.move()
        self.collisions()
        win.screen.blit(self.image_rotation, self.rect)

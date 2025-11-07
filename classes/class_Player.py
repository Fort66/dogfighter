import pygame as pg

from pygame.transform import scale_by
from pygame.image import load

from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_a, K_s, K_d, K_c

from pygame.sprite import Sprite, Group, groupcollide
from pygame.math import Vector2

from icecream import ic

from time import time

# pg.init()

from .class_AllSprites import all_sprites
from .class_PlayerShoot import PlayerShoot
from .class_Rockets import rockets_group
from .class_Explosions import Explosions
from .class_Screen import win


player_group = Group()
player_rockets_group = Group()
explosion_group = Group()


class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = scale_by(load("images/su-33.png").convert_alpha(), 0.3)
        # self.image.fill('SteelBlue')
        self.rect = self.image.get_rect(
            center=(win.screen.get_width() // 2, win.screen.get_height() // 2)
        )
        self.speed = 5
        self._layer = 2
        self.shoot_time = 1
        self.permission_shoot = 1
        self.direction_x = 0
        player_group.add(self)
        all_sprites.add(self)

    def move(self):
        keys = pg.key.get_pressed()

        if keys[K_UP] or keys[K_w]:
            self.rect.move_ip(0, -self.speed) if self.rect.top > 0 else None

        if keys[K_DOWN] or keys[K_s]:
            (
                self.rect.move_ip(0, self.speed)
                if self.rect.bottom < win.screen.get_height()
                else None
            )

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

        if keys[K_c]:
            if not self.shoot_time:
                self.shoot_time = time()
            if time() - self.shoot_time >= self.permission_shoot:
                shoot = PlayerShoot(
                    pos=(self.rect.centerx - 46, self.rect.centery + 15),
                    speed=self.speed * 2,
                )
                player_rockets_group.add(shoot)
                all_sprites.add(shoot)
                self.shoot_time = time()

    def collisions(self):
        rocket_collide = groupcollide(rockets_group, player_rockets_group, True, True)
        if rocket_collide:
            hits = list(rocket_collide.keys())[0]
            ic(hits)
            self.explosion_rocket = Explosions(win.screen, hits.rect.center, 1)
            self.explosion_rocket.speed = hits.speed * hits.direction_x

        player_collide = groupcollide(player_group, rockets_group, True, True)
        if player_collide:
            self.explosion_player = Explosions(win.screen, self.rect.center, 2)
            self.explosion_player.speed = self.speed * self.direction_x
            # if self.explosion_player.image._ended:
            #     player_collide.clear()
            #     all_sprites.remove(self)

    def update(self):
        self.move()
        self.collisions()
        win.screen.blit(self.image, self.rect)

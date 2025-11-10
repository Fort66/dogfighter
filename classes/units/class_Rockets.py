# import pygame as pg
import gif_pygame as gif

from random import choice, uniform

from pygame.sprite import Sprite

from ..groups.class_AllSprites import all_sprites
from ..screens.class_Screen import win
from ..groups.class_SpritesGroups import groups


class Enemies(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = gif.load('images/supawork3.gif')
        self.image = gif.transform.scale_by(self.image, .4, new_gif=True)
        # self.image.fill('DarkRed')
        self.speed = uniform(5, 15)
        self.gen_pos()
        self._layer = 2
        self.direction_x = 0
        groups.rockets_group.add(self)
        all_sprites.add(self)

    def gen_pos(self):
        self.rect = self.image.get_rect(center=(
            uniform(win.screen.get_width() + 1000, win.screen.get_width() + 3000), # x
            uniform(0, win.screen.get_height()) # y
        ))

    def move(self):
        self.rect.move_ip(-self.speed, 0)
        self.direction_x = -1

        if self.rect.left <= -100:
            # rockets_group.remove(self)
            self.gen_pos()

    def update(self):
        self.move()
        # self.scr.blit(self.image, self.rect)
        self.image.render(win.screen, self.rect)
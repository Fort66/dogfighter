from pygame.image import load
from pygame.transform import scale_by, flip
from pygame.sprite import Sprite

from random import choice, uniform

from .class_AllSprites import all_sprites
from .class_Screen import win
from .class_SpritesGroups import groups

enemies = [
    ['images/plane1.png', (0, 0), .18],
    ['images/plane2.png', (0, 0), .15],
    ['images/plane3.png', (0, 0), .15],
    ['images/plane4.png', (0, 0), .2],
    ['images/plane5.png', (0, 0), .2],
]


class Enemies(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        enemy = choice(enemies)
        self.image = scale_by(load(enemy[0]).convert_alpha(), enemy[-1])
        self.speed = uniform(5, 10)
        self.gen_pos()
        self._layer = 2
        self.direction_x = 0
        groups.enemies_group.add(self)
        all_sprites.add(self)

    def gen_pos(self):
        self.rect = self.image.get_rect(center=(
            uniform(win.screen.get_width() + 1000, win.screen.get_width() + 3000), # x
            uniform(0, win.screen.get_height()) # y
        ))

    def move(self):
        self.rect.move_ip(-self.speed, 0)
        self.direction_x = -1

        if self.rect.left <= -1000:

            self.gen_pos()

    def update(self):
        self.move()
        win.screen.blit(self.image, self.rect)
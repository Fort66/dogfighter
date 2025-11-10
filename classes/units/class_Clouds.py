from pygame.transform import scale_by
from pygame.image import load
from pygame.sprite import Sprite, Group

from random import uniform, randint, choice

from ..groups.class_AllSprites import all_sprites
from ..screens.class_Screen import win

cloud_group = Group()

# lst_layers = ['move_to_front', 'move_to_back',]

class Clouds(Sprite):
    def __init__(self, path):
        Sprite.__init__(self)
        self._layer = randint(1, 3)
        match self._layer:
            case 1:
                self.scale_value = 0.4
            case 2:
                self.scale_value = 0.6
            case 3:
                self.scale_value = .8
        self.image = scale_by(load(path).convert_alpha(), self.scale_value)
        self.rect = self.image.get_rect()
        self.speed = uniform(1, 3)
        self.gen_pos()
        cloud_group.add(self)
        all_sprites.add(self)

    def gen_pos(self):
        self.rect = self.image.get_rect(center=(
            uniform(win.screen.get_width() + 1000, win.screen.get_width() + 5000), # x
            uniform(0, win.screen.get_height()) # y
        ))


    def move(self):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.left < -2000:
            # cloud_group.remove(self)
            self.gen_pos()

    def update(self):
        self.move()
        # self.get_layer_of_sprite()
        win.screen.blit(self.image, self.rect)
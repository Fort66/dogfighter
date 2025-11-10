import gif_pygame as gif

from pygame.sprite import Group, Sprite

# from classes.class_Rockets import Rocket
# from classes.class_AllSprites import all_sprites

# player_rockets_group = Group()
from ..screens.class_Screen import win

class PlayerShoot(Sprite):
    def __init__(self, pos, speed):
        Sprite.__init__(self)
        self.pos = pos
        self.image = gif.load('images/supawork3.gif')
        self.image = gif.transform.flip(self.image, flip_x=True, flip_y=False, new_gif=True)
        self.image = gif.transform.scale_by(self.image, .4, new_gif=True)
        self.speed = speed
        self._layer = 2
        self.direction_x = 0
        self.gen_pos()
        # player_rockets_group.add(self)
        # all_sprites.add(self)

    def move(self):
        self.rect.move_ip(self.speed, 0)
        self.direction_x = 1
        if self.rect.right > win.screen.get_width() + 200:
            self.kill()

    def gen_pos(self):
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.move()
        self.image.render(win.screen, self.rect)
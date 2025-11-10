from pygame.sprite import Group, GroupSingle, Sprite

from icecream import ic


class AllSprites(Group):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def update(self, *args, **kwargs):
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite._layer):
            sprite.update(*args, **kwargs)



all_sprites = AllSprites()
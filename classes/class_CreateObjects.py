from random import choice

from .class_Player import Player
from .class_Enemies import Enemies
from .class_Clouds import Clouds
from .class_LevelsGame import levels_game


clouds_images = [
    # 'images/cloud1.png',
    'images/cloud2.png',
    'images/cloud3.png',
    'images/cloud4.png',
    'images/cloud5.png',
    # 'images/cloud6.png'
    ]


class CreateObjects:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def create(self):
        self.player = Player()
        self.enemies = [Enemies() for i in range(levels_game.enemies_amount)]
        self.clouds = [Clouds(choice(clouds_images)) for _ in range(15)]

create_objects = CreateObjects()
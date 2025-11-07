import pygame as pg
import pygame_widgets as pw

from pygame.locals import QUIT, K_ESCAPE, KEYDOWN, K_F2


from icecream import ic

# from OpenGL.GL import *
# from OpenGL.GLU import *

from classes.class_Player import Player, player_group
from classes.class_Rockets import Rocket, rockets_group
from classes.class_Clouds import Clouds, cloud_group
from .class_Screen import win
from classes.class_AllSprites import all_sprites
from .class_StartScreen import StartScreen
from .class_PauseScreen import PauseScreen
from .class_GameOverScreen import GameOverScreen

from random import choice, randint
import os

# os.environ['SDL_VIDEODRIVER'] = 'x11'
# export SDL_VIDEODRIVER=wayland
pg.init()

# ic(os.getenv('SDL_VIDEODRIVER'))



clouds_images = [
    # 'images/cloud1.png',
    'images/cloud2.png',
    'images/cloud3.png',
    'images/cloud4.png',
    'images/cloud5.png',
    # 'images/cloud6.png'
    ]

start_screen = StartScreen()
pause_screen = PauseScreen()
game_over = GameOverScreen()
player = Player()
rockets = [Rocket() for i in range(16)]
clouds = [Clouds(choice(clouds_images)) for _ in range(15)]


class Game:
    def __init__(self):
        self.loop = True
        self.fps = 60
        self.clock = pg.time.Clock()

    def run(self):
        while self.loop:
            win.screen.fill('SkyBlue')
            events = pg.event.get()
            for event in events:
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.loop = False
                # elif event.type == KEYDOWN and event.key == K_F2:
                #     pause_screen.change_pause()


            if start_screen.start:
                # start_screen.transfer_events(events)
                # pw.update(events)
                start_screen.update()

            # if pause_screen.pause:
            #     pause_screen.update()

            # if game_over.game_over:
            #     game_over.update()
            else:
                all_sprites.update()

            # if len(player_group) <= 0:
            #     # if not game_over.game_over:
            #     #     for sprite in all_sprites:
            #     #         if sprite in explosion_group and sprite._:
            #     if not game_over.game_over:
            #         game_over.change_game_over()


            # pw.update(events)
            pg.display.update()
            self.clock.tick(self.fps)
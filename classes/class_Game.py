import pygame as pg
import pygame_widgets as pw

from pygame.locals import QUIT, K_ESCAPE, KEYDOWN, K_F2


from icecream import ic
import os

# from OpenGL.GL import *
# from OpenGL.GLU import *

from .class_Screen import win
from .class_AllSprites import all_sprites
from .class_StartScreen import start_screen
from .class_PauseScreen import pause_screen
from .class_GameOverScreen import game_over_screen
from .class_CreateObjects import create_objects
from .class_SpritesGroups import groups
from .class_Signals import signals



# os.environ['SDL_VIDEODRIVER'] = 'x11'
# export SDL_VIDEODRIVER=wayland
pg.init()

# ic(os.getenv('SDL_VIDEODRIVER'))




class Game:
    def __init__(self):
        self.loop = True
        self.fps = 60
        self.clock = pg.time.Clock()
        # self.setup()

    def clear_groups(self):
        groups.clear()
        all_sprites.empty()

    def run(self):
        while self.loop:
            win.screen.fill('SkyBlue')
            events = pg.event.get()
            for event in events:
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.loop = False
                elif event.type == KEYDOWN and event.key == K_F2:
                    signals.change_signals('pause')


            if signals.start:
                start_screen.update()

            elif signals.pause:
                pause_screen.update()

            elif signals.game_over:
                self.clear_groups()
                game_over_screen.update()

            else:
                all_sprites.update()

            # if len(groups.player_group) <= 0:
            #     # if not game_over.game_over:
            #     #     for sprite in all_sprites:
            #     #         if sprite in explosion_group and sprite._:
            #     if not game_over.game_over:
            #         game_over.change_game_over()


            # pw.update(events)
            pg.display.update()
            self.clock.tick(self.fps)
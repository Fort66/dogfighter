import pygame as pg
from pygame.locals import *
from pygame.image import load
from pygame.transform import scale, flip
from pygame import MOUSEMOTION
from pygame.mouse import get_pos, get_pressed
from pygame.sprite import Sprite
from pygame import Surface

from sys import platform
from icecream import ic


pg.init()

# @dataclass
class ButtonText:
    def __init__(self, surface=None, pos=(0, 0), size=(50, 5), **kwargs):
        self.surface = surface
        self.pos: tuple = pos #kwargs.get('pos', (0, 0))
        self.size: list|tuple = size #kwargs.get('size', (50, 5))

        self.text: str = kwargs.get('text', 'Example')
        self.font: str = kwargs.get('font', None)
        self.font_size: int = kwargs.get('font_size', 26)

        self.disabled_color: str|tuple = kwargs.get('disabled_color','#2F4F4F')
        self.bg_color: str|tuple = kwargs.get('bg_color','#0B61A4')
        self.text_color: str|tuple = kwargs.get('text_color','#FFFFFF')
        self.hover_color: str|tuple = kwargs.get('hover_color','#033E6B')
        self.click_color: str|tuple = kwargs.get('click_color','#66A3D2')
        self.color: str|tuple = kwargs.get('color', self.bg_color)

        self.rounding: int = kwargs.get('rounding',0)

        self.on_enabled: bool = kwargs.get('on_enabled', True)
        self.is_hovered: bool = kwargs.get('is_hovered', False)
        self.allow_clicking: bool = kwargs.get('allow_clicked', True)
        self.on_click: object = kwargs.get('on_click', lambda *args, **kwargs: None)
        ic(self.__dict__)

        self.__post_init__(self)

    def __post_init__(self, font: str):
        self.rect = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        if platform == 'win32':
            self.font = pg.font.Font(self.font, self.font_size) if self.font else pg.font.SysFont('Arial', self.font_size)

        elif platform == 'linux' or platform == 'linux2':
            self.font = pg.font.Font(self.font, self.font_size) if self.font else pg.font.SysFont('Arial', self.font_size)

        elif platform == 'darwin':
            self.font = pg.font.Font(self.font, self.font_size) if self.font else pg.font.SysFont('Sans-serif', self.font_size)

    def handleEvent(self):#, event):
        self.keys = get_pressed()
        if self.on_enabled:
            if MOUSEMOTION:
                self.is_hovered = self.rect.collidepoint(get_pos())
                # if self.is_hovered:
                #     self.color = self.hover_color
            # if MOUSEBUTTONDOWN:
            #     print(MOUSEBUTTONDOWN)
            if self.keys[0] and self.is_hovered:
                # self.color = self.click_color
                if self.allow_clicking and self.on_click:
                    self.on_click()
                    self.allow_clicking = False
            else:
            #     self.color = self.bg_color
                self.allow_clicking = True

    def update(self):
        self.handleEvent()
        if self.keys[0] and self.is_hovered:
            self.color = self.click_color
            ic(self. color)
        if self.is_hovered:
            self.color = self.hover_color
        else:
            self.color = self.bg_color

        self.rounded_rect = pg.draw.rect(self.surface, self.color, self.rect, border_radius = self.rounding)

        if self.text:
            if self.on_enabled:
                text_surface = self.font.render(self.text, True, self.text_color)
            else:
                text_surface = self.font.render(self.text, True, self.disabled_color)
                text_surface.fill(self.disabled_color, special_flags = pg.BLEND_RGBA_MULT)
            text_rect = text_surface.get_rect(center = self.rounded_rect.center)
            self.surface.blit(text_surface, text_rect)

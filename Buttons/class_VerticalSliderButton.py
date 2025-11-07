import pygame as pg
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import Surface
from pygame.transform import scale

from dataclasses import dataclass


@dataclass
class VerticalSliderButton:
    pos: tuple = (0, 0)
    size: tuple = (50, 200)
    min_value: int | float = 0
    max_value: int | float = 100
    current_value: int | float = 50
    color_button: str | tuple = 'LightGray'
    color_scale_left: str | tuple = 'green'
    hover_color_slider: str | tuple = 'red'
    color_slider: str | tuple = 'Maroon'
    hover_color: str | tuple = 'darkgray'
    text_color: str | tuple = 'white'
    disabled_color: str | tuple = 'darkgray'

    isHovered: bool = False
    isClicked: bool = False
    onEnabled: bool = True

    def __post_init__(self):
        self.buttonSurface = Surface(self.size, pg.SRCALPHA)
        self.buttonSurface.set_alpha(0)
        self.buttonSurface.fill(self.color_button)
        self.buttonRect = self.buttonSurface.get_rect(topleft = self.pos)

        self.scaleSurface = Surface((self.size[0] // 10, self.size[1]), pg.SRCALPHA)
        self.scaleSurface.set_alpha(70)
        self.scaleSurface.fill(self.color_button)
        self.scaleRect = self.scaleSurface.get_rect(center = self.buttonRect.center)

        self.sliderSurface = Surface((self.size[0] // 2, self.size[1] // 20), pg.SRCALPHA)
        self.sliderSurface.fill(self.color_slider)

        self.oneStepValue = (self.scaleRect.bottom - self.scaleRect.top) / (self.max_value - self.min_value)

        self.sliderRect = self.sliderSurface.get_rect(center = (self.scaleRect.x + self.current_value * self.oneStepValue, self.scaleRect.centery))

        self.sliderRect = self.sliderSurface.get_rect(center = (self.scaleRect.centerx, self.scaleRect.bottom - self.current_value * self.oneStepValue))

        self.createBottomSurface()
        self.changeCurrent_value()

    def createBottomSurface(self):
        if self.sliderRect.bottom < self.scaleRect.bottom:
            self.scaleSurfaceBottom = scale(self.scaleSurface.copy(), (self.scaleRect.width, self.scaleRect.bottom - self.sliderRect.bottom))
        else:
            self.scaleSurfaceBottom = Surface((0, 0))
        self.scaleSurfaceBottom.set_alpha(256)
        if self.onEnabled:
            self.scaleSurfaceBottom.fill(self.color_scale_left)
        else:
            self.scaleSurfaceBottom.fill(self.disabled_color)
        self.scaleRectBottom = self.scaleSurfaceBottom.get_rect(bottomleft = self.scaleRect.bottomleft)

    def changeCurrent_value(self):
        self.current_value = (self.scaleRect.bottom - self.sliderRect.centery) / self.oneStepValue

        self.scaleRectBottom.width = self.sliderRect.left - self.scaleRect.left
        self.scaleRectBottom.topleft = self.scaleRect.topleft
        self.createBottomSurface()

        print(self.current_value)

    def checkPosition(self, event):
        self.sliderRect.center = (self.sliderRect.center[0], event.pos[1])
        if self.sliderRect.centery <= self.buttonRect.top:
            self.sliderRect.centery = self.buttonRect.top
        if self.sliderRect.centery >= self.buttonRect.bottom:
            self.sliderRect.centery = self.buttonRect.bottom

    def handleEvent(self, event):
        if self.onEnabled:
            if self.isClicked:
                if event.type == MOUSEMOTION:
                    self.checkPosition(event)
                    self.changeCurrent_value()

            if event.type == MOUSEMOTION:
                if self.sliderRect.collidepoint(event.pos):
                    self.isHovered = True
                    self.sliderSurface.fill(self.hover_color_slider)
                else:
                    self.isHovered = False
                    self.sliderSurface.fill(self.color_slider)
            if event.type == MOUSEBUTTONDOWN and self.isHovered:
                if event.button == 1:
                    self.isClicked = True
            elif event.type == MOUSEBUTTONDOWN and self.scaleRect.collidepoint(event.pos):
                if event.button == 1:
                    self.sliderRect.center = (self.sliderRect.center[0], event.pos[1])
                    self.changeCurrent_value()

            elif event.type == MOUSEBUTTONUP:
                self.isClicked = False
        else:
            self.sliderSurface.fill(self.disabled_color)

    def drawText(self, surface):
        minText = pg.font.SysFont('arial', 14).render(str(self.min_value), True, self.text_color)
        maxText = pg.font.SysFont('arial', 14).render(str(self.max_value), True, self.text_color)
        valueText = pg.font.SysFont('arial', 14).render(str(self.current_value), True, self.text_color)

        surface.blit(minText, (self.scaleRect.x, self.scaleRect.bottom + maxText.get_width()))
        surface.blit(maxText, (self.scaleRect.x, self.scaleRect.top - maxText.get_width()))
        surface.blit(valueText, (self.buttonRect.left - valueText.get_width(), self.sliderRect.centery - valueText.get_height() // 2))

    def update(self, surface):
        surface.blit(self.buttonSurface, self.buttonRect)
        surface.blit(self.scaleSurfaceBottom, self.scaleRectBottom)
        surface.blit(self.scaleSurface, self.scaleRect)
        surface.blit(self.sliderSurface, self.sliderRect)
        self.drawText(surface)
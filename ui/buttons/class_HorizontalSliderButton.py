import pygame as pg
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import Surface
from pygame.transform import scale

from dataclasses import dataclass


@dataclass
class HorizontalSliderButton:
    pos: tuple = (0, 0)
    size: tuple = (200, 50)
    min_value: int | float = 0
    max_value: int | float = 100
    current_value: int | float = 50
    colorButton: str | tuple = 'LightGray'
    colorScaleLeft: str | tuple = 'green'
    hoverColorSlider: str | tuple = 'red'
    colorSlider: str | tuple = 'Maroon'
    hoverColor: str | tuple = 'darkgray'
    textColor: str | tuple = 'white'
    disabledColor: str | tuple = 'darkgray'

    isHovered: bool = False
    isClicked: bool = False
    onEnabled: bool = True

    def __post_init__(self):
        self.buttonSurface = Surface(self.size, pg.SRCALPHA)
        self.buttonSurface.set_alpha(0)
        self.buttonSurface.fill(self.colorButton)
        self.buttonRect = self.buttonSurface.get_rect(topleft = self.pos)

        self.scaleSurface = Surface((self.size[0], self.size[1] // 10), pg.SRCALPHA)
        self.scaleSurface.set_alpha(70)
        self.scaleSurface.fill(self.colorButton)
        self.scaleRect = self.scaleSurface.get_rect(center = self.buttonRect.center)

        self.sliderSurface = Surface((self.size[0] // 20, self.size[1] // 2))
        self.sliderSurface.fill(self.colorSlider)

        self.oneStepValue = (self.scaleRect.right - self.scaleRect.left) / (self.max_value - self.min_value)

        self.sliderRect = self.sliderSurface.get_rect(center = (self.scaleRect.x + self.current_value * self.oneStepValue, self.scaleRect.centery))

        self.createLeftSurface()
        self.changeCurrentValue()


    def createLeftSurface(self):
        if self.sliderRect.left > self.scaleRect.left:
            self.scaleSurfaceLeft = scale(self.scaleSurface.copy(), (self.sliderRect.left - self.scaleRect.left, self.scaleRect.height))
        else:
            self.scaleSurfaceLeft = Surface((0, 0))
        self.scaleSurfaceLeft.set_alpha(256)
        if self.onEnabled:
            self.scaleSurfaceLeft.fill(self.colorScaleLeft)
        else:
            self.scaleSurfaceLeft.fill(self.disabledColor)
        self.scaleRectLeft = self.scaleSurfaceLeft.get_rect(topleft = self.scaleRect.topleft)

    def changeCurrentValue(self):
        self.current_value = (self.sliderRect.centerx - self.scaleRect.x) / self.oneStepValue

        self.scaleRectLeft.width = self.sliderRect.left - self.scaleRect.left
        self.scaleRectLeft.topleft = self.scaleRect.topleft
        self.createLeftSurface()

        print(self.current_value)


    def checkPosition(self, event):
        self.sliderRect.center = (event.pos[0], self.sliderRect.center[1])
        if self.sliderRect.centerx >= self.buttonRect.right:
            self.sliderRect.centerx = self.buttonRect.right
        if self.sliderRect.centerx <= self.buttonRect.left:
            self.sliderRect.centerx = self.buttonRect.left


    def handleEvent(self, event):
        if self.onEnabled:
            if self.isClicked:
                if event.type == MOUSEMOTION:
                    self.checkPosition(event)
                    self.changeCurrentValue()

            if event.type == MOUSEMOTION:
                if self.sliderRect.collidepoint(event.pos):
                    self.isHovered = True
                    self.sliderSurface.fill(self.hoverColorSlider)
                else:
                    self.isHovered = False
                    self.sliderSurface.fill(self.colorSlider)
            if event.type == MOUSEBUTTONDOWN and self.isHovered:
                if event.button == 1:
                    self.isClicked = True
            elif event.type == MOUSEBUTTONDOWN and self.scaleRect.collidepoint(event.pos):
                if event.button == 1:
                    # self.sliderRect.center = (event.pos[0], self.sliderRect.center[1])
                    self.checkPosition(event)
                    self.changeCurrentValue()

            elif event.type == MOUSEBUTTONUP:
                self.isClicked = False
        else:
            self.sliderSurface.fill(self.disabledColor)

    def drawText(self, surface):
        minText = pg.font.SysFont('arial', 14).render(str(self.min_value), True, self.textColor)
        maxText = pg.font.SysFont('arial', 14).render(str(self.max_value), True, self.textColor)
        valueText = pg.font.SysFont('arial', 14).render(str(self.current_value), True, self.textColor)

        surface.blit(minText, (self.scaleRect.left - maxText.get_width(), self.scaleRect.y))
        surface.blit(maxText, (self.scaleRect.right + maxText.get_width(), self.scaleRect.y))
        surface.blit(valueText, (self.sliderRect.centerx - valueText.get_width() // 2, self.buttonRect.top - valueText.get_height()))

    def update(self, surface):
        surface.blit(self.buttonSurface, self.buttonRect)
        surface.blit(self.scaleSurfaceLeft, self.scaleRectLeft)
        surface.blit(self.scaleSurface, self.scaleRect)
        surface.blit(self.sliderSurface, self.sliderRect)
        self.drawText(surface)
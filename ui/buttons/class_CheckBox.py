import pygame
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, QUIT

from dataclasses import dataclass, field, InitVar

@dataclass
class CheckBox:
    screen: object = None

    pos: tuple = field(default = (0, 0))
    size: tuple = field(default = (0, 0))

    text: str = field(default = "")
    font: object = field(default = None)
    color: str | tuple[int, int, int] = 'white'

    disabledColor: str | tuple[int, int, int] = 'dimgrey'
    checkedСolor: str | tuple[int, int, int] = 'red'
    hoverСolor: str | tuple[int, int, int] = 'blue'

    onEnabled: bool = True
    checked: bool = field(default = False)
    hovered: bool = field(default = False)

    onCheckedReference: object = None
    notCheckedReference: object = None
    checkedArgs: tuple = field(default_factory = tuple)
    checkedKwargs: dict = field(default_factory = dict)
    notCheckedArgs: tuple = field(default_factory = tuple)
    notCheckedKwargs: dict = field(default_factory = dict)

    def __post_init__(self):
        if self.size[0] < 20 or self.size[1] < 20:
            self.size = (20, 20)
        self.rect = pygame.Rect(self.pos, self.size)
        self.innerRect = self.rect.inflate(-10, -10)

    def update(self, screen):
        if self.onEnabled:
            pygame.draw.rect(screen, self.hoverСolor if self.hovered else self.color, self.rect, 2)
            if self.checked:
                # pygame.draw.rect(screen, self.checkedСolor, self.rect, width =  2)
                pygame.draw.rect(screen, self.checkedСolor, self.innerRect)
            text_surface = self.font.render(self.text, True, self.hoverСolor if self.hovered else self.color)
        else:
            pygame.draw.rect(screen, self.disabledColor, self.rect, 2)
            text_surface = self.font.render(self.text, True, self.disabledColor)
        text_rect = text_surface.get_rect()
        text_rect = text_surface.get_rect(topleft = (self.rect.right + 10, self.rect.centery - text_surface.get_height() // 2))
        screen.blit(text_surface, text_rect)

    def handleEvent(self, event):
        if self.onEnabled:
            if event.type == MOUSEMOTION:
                self.hovered = self.rect.collidepoint(event.pos)
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(event.pos):
                    self.checked = not self.checked
                    if self.onCheckedReference and self.checked:
                        self.onCheckedReference(*self.checkedArgs, **self.checkedKwargs)
                    elif self.notCheckedReference and not self.checked:
                        if self.notCheckedReference:
                            self.notCheckedReference(*self.notCheckedArgs, **self.notCheckedKwargs)



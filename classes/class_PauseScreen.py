from pygame.image import load
from pygame.transform import scale
from pygame_widgets.textbox import TextBox
# from ui.class_ButtonText import ButtonText
from icecream import ic

from .class_Screen import win

class PauseScreen:
    def __init__(self):
        self.pause = False
        self.image =scale(load('images/screens/pause.jpg').convert(), win.screen.get_size())
        self.rect = self.image.get_rect()

        self.label = TextBox(
            win.screen,
            win.screen.get_width() //2 - 100,
            win.screen.get_height() // 2 - 50,
            width=250,
            height=50,
            placeholderText='F2 - продолжить игру',
            colour=(70, 130, 180),
            borderColour=(23, 74, 117),
            placeholderTextColour='white',
        )


    def change_pause(self):
        self.pause = not self.pause


    def update(self):
        win.screen.blit(self.image, self.rect)
        # self.label.draw()
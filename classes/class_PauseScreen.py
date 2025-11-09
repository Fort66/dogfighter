from pygame.image import load
from pygame.transform import scale
from icecream import ic
# from pygame_widgets.textbox import TextBox
from Buttons.class_ButtonText import ButtonText
from .class_Screen import win
from .class_Signals import signals

class PauseScreen:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.image =scale(load('images/screens/pause.jpg').convert(), win.screen.get_size())
        self.rect = self.image.get_rect()

        self.btn = ButtonText(
            surface=self.image,
            pos=(self.rect[2] //2, self.rect[3] - 200),
            size=(200, 50),
            text='F2 - продолжить',
            on_enabled=False,
        )


    def change_pause(self):
        signals.change_signals('pause')


    def update(self):
        win.screen.blit(self.image, self.rect)
        self.btn.update()


pause_screen = PauseScreen()
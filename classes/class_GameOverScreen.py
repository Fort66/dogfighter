from pygame.image import load
from pygame.transform import scale
# from pygame_widgets.button import Button, ButtonArray
# from pygame_widgets.textbox import TextBox
from icecream import ic

from Buttons.class_ButtonText import ButtonText
from .class_Signals import signals
from .class_Screen import win

class GameOverScreen:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.image =scale(load('images/screens/game_over.jpeg').convert(), win.screen.get_size())
        self.rect = self.image.get_rect()

        self.btn = ButtonText(
            surface=self.image,
            pos=(self.rect[2] //2, self.rect[3] - 200),
            size=(800, 50),
            text='Разбился и сгорел!!! Начать игру снова? Esc - выйти.',
            on_click=lambda: self.change_game_over(),
            rounding=20,
        )

    def change_game_over(self):
        signals.change_signals('game_over')
        if self.btn.is_clicked:
            signals.change_signals('start')

    def transfer_events(self, events):
        self.events = events

    def update(self):
        win.screen.blit(self.image, self.rect)
        self.btn.update()


game_over_screen = GameOverScreen()
from pygame.image import load
from pygame.transform import scale
from pygame_widgets.button import Button, ButtonArray
from pygame_widgets.textbox import TextBox

from icecream import ic
from .class_Screen import win

class GameOverScreen:
    def __init__(self):
        self.game_over = False
        self.image =scale(load('images/screens/game_over.jpeg').convert(), win.screen.get_size())
        self.rect = self.image.get_rect()

        self.label = TextBox(
            win,
            win.screen.get_width() //2 - 100,
            win.screen.get_height() // 2 - 150,
            width=250,
            height=50,
            placeholderText='Разбился и сгорел!',
            colour=(70, 130, 180),
            borderColour=(23, 74, 117),
            placeholderTextColour='white',
        )

        self.btn = Button(
            win.screen,
            x=win.screen.get_width() //2 - 100,
            y=win.screen.get_height() // 2 + 50,
            width=200,
            height=50,
            text='Начать игру',
            onClick=lambda:self.change_game_over(),
            colour=(70, 130, 180),
            hoverColour=(23, 74, 117),
            radius=20,
            textColour='white'
        )


    def change_game_over(self):
        self.game_over = not self.game_over

    def transfer_events(self, events):
        self.events = events

    def update(self):
        win.screen.blit(self.image, self.rect)
        # self.btn.listen(self.events)
        # self.label.draw()
        # self.btn.draw()
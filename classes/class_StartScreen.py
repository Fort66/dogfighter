from pygame.image import load
from pygame.transform import scale
from pygame_widgets.button import Button, ButtonArray

from icecream import ic

from .class_Screen import win
from Buttons.class_ButtonText import ButtonText

class StartScreen:
    def __init__(self):
        self.start = True
        self.image =scale(load('images/screens/start.jpg').convert(), win.screen.get_size())
        self.rect = self.image.get_rect()
        # self.btn = Button(
        #     win.screen,
        #     x=win.screen.get_width() //2 - 100,
        #     y=win.screen.get_height() - 200,
        #     width=200,
        #     height=50,
        #     text='Начать игру',
        #     onClick=lambda:self.change_start(),
        #     colour=(70, 130, 180),
        #     hoverColour=(23, 74, 117),
        #     radius=20,
        #     textColour='white'
        # )
        self.btn = ButtonText(
            pos=(win.screen.get_width() //2 - 100,
            win.screen.get_height() - 200),
            size=(200, 50),
            bgColor=(70, 130, 180),
            textColor='white',
            text='Начать игру',
            hoverColor=(23, 74, 117),
            rounding=20,
            onClickReference=self.change_start
        )


    def change_start(self):
        self.start = not self.start

    # def transfer_events(self, events):
    #     self.events = events

    def update(self):
        win.screen.blit(self.image, self.rect)
        self.btn.update(self.image)
        # self.btn.listen(self.events)
        # self.btn.draw()
        # self.btn.update(self.events)


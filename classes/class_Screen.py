from pygame.display import set_mode, set_caption, get_desktop_sizes
from pygame.locals import QUIT, K_ESCAPE, KEYDOWN, FULLSCREEN, DOUBLEBUF, OPENGL, OPENGLBLIT

class Screen:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        # self. size = get_desktop_sizes()[0]
        self. size = ([1920, 1080])

        self.screen = set_mode(self.size, DOUBLEBUF)
        self.caption = set_caption('MyGame')




win = Screen()
class Singals:
    __signals = {
        'start': True,
        'pause': False,
        'game_over': False
    }

    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__dict__ = self.__signals

    def change_signals(self, signal):
        self.__dict__[signal] = not self.__dict__[signal]

signals = Singals()
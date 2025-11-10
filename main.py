from pygame import quit

from icecream import ic

from classes.logic.class_Game import Game

# from loguru import logger

def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
    quit()

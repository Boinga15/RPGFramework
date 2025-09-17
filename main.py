import threading

from framework import *

def gameStart(game: Game):
    input("> ")

    # Closing the game.
    game.quit()

if __name__ == "__main__":
    game = Game()

    newThread = threading.Thread(target=gameStart, args=(game,))
    newThread.start()
    game.handleLoop()

    newThread.join()
    quit()
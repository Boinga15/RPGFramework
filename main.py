import threading
import os

from framework import * 

# Game Functions
def gameStart(game: Game):
    os.system("cls")

    # Any code for the actual game should be written here.

    # Closing the game.
    game.quit()

if __name__ == "__main__":
    game = Game()

    newThread = threading.Thread(target=gameStart, args=(game,))
    newThread.start()
    game.handleLoop()

    newThread.join()
    quit()
import threading
import os

from framework import *

def gameStart(game: Game):
    os.system("cls")

    game.writeText("This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works.")
    game.writeText("This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works.")
    game.infoText("Health: 100")
    input("> ")

    game.clearStory()
    game.writeText("This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works.")
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
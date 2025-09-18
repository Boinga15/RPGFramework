import threading
import os

from framework import *

def gameStart(game: Game):
    os.system("cls")

    game.party.append(Character("Agent", 100))

    game.writeText("This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works.")
    game.infoText("Health: 100")
    input("> ")

    game.party[0].addItem(TestItem(), 8)
    game.party[0].addItem(TestItem(), 9999)
    game.party[0].removeItems(TestItem, 3)

    game.clearStory()
    game.writeText("This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works. This is a test to see how well the code written works.")
    
    game.clearInfo()
    for character in game.party:
        game.infoText(f"{character.name}:")
        game.infoText(f"Health: {character.health} / {character.getMaxHealth()}")

        game.infoText("")
        game.infoText("Inventory:")
        for item in character.inventory:
            if item.quantity == 1:
                game.infoText(f"{item.name}")
            else:
                game.infoText(f"{item.name} (X{item.quantity})")
    
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
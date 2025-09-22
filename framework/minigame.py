import os
import threading
import time
import keyboard
import random

# Starts a mash minigame where the player must press space or A & D as fast as they can in the given time limit. Returns the amount of times they pressed the button in the time limit.
def mashMinigame(givenTime = 5, useSpace = True):
    os.system("cls")

    mashAmount = 0
    timeLeft = givenTime

    def handleDisplay():
        os.system("cls")
        print(f"Time Left: {timeLeft}")
        print(f"Mash Amount: {mashAmount}")

        if useSpace:
            print("\nMash space!")
        
        else:
            print("\nMash A and D!")

    def reduceTime():
        nonlocal mashAmount, timeLeft

        keyPressedId = 0

        while timeLeft > 0:
            if useSpace:
                if keyboard.is_pressed("space") and keyPressedId == 0:
                    keyPressedId = 1
                    mashAmount += 1
                    handleDisplay()
                
                elif not keyboard.is_pressed("space"):
                    keyPressedId = 0
            
            else:
                if keyboard.is_pressed("A") and keyPressedId == 0:
                    keyPressedId = 1
                    mashAmount += 1
                    handleDisplay()
                
                elif keyboard.is_pressed("D") and keyPressedId == 1:
                    keyPressedId = 0
                    mashAmount += 1
                    handleDisplay()
                


    timerThread = threading.Thread(target = reduceTime, args = ())
    timerThread.start()

    while timeLeft > 0:
            timeLeft -= 0.1
            handleDisplay()

            time.sleep(0.1)
    
    os.system("cls")
    timerThread.join()

    return mashAmount

# Starts a reaction-based minigame, where the player must press space after a short delay. Returns the time it took for the player to react and press space.
def reactionMinigame():
    os.system("cls")
    print("Wait...")

    time.sleep(random.uniform(2, 5))

    os.system("cls")
    print("Press space!")
    t1 = time.time()

    # Make sure that they aren't holding space down.
    while keyboard.is_pressed("space"):
        pass

    # Now wait for them to press space again.
    while not keyboard.is_pressed("space"):
        pass

    t2 = time.time()
    elapsedTime = t2 - t1

    return elapsedTime
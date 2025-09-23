import os
import threading
import time
import keyboard
import random
import math
import msvcrt


# A helper function used after every minigame to clear the input buffer.
def flushBuffer():
    while msvcrt.kbhit():
        msvcrt.getch()

# Starts a mash minigame where the player must press space or A & D as fast as they can in the given time limit. Returns the amount of times they pressed the button in the time limit.
def mashMinigame(givenTime = 5, useSpace = True):
    os.system("cls")

    mashAmount = 0
    timeLeft = givenTime

    def handleDisplay():
        os.system("cls")
        print(f"Time Left: {math.ceil(timeLeft * 10) / 10}")
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

    flushBuffer()

    return mashAmount

# Starts a reaction-based minigame, where the player must press space after a short delay. Returns the time it took for the player to react and press space.
def reactionMinigame():
    os.system("cls")
    print("Wait...")

    penalty = 0

    stallTimer = random.uniform(2, 5)

    while stallTimer > 0:
        stallTimer -= 0.01

        if keyboard.is_pressed("space"):
            penalty += 0.1

        time.sleep(0.01)

    os.system("cls")
    print("Press space!")
    t1 = time.time()

    # Now wait for them to press space again.
    while not keyboard.is_pressed("space"):
        pass

    t2 = time.time()
    elapsedTime = t2 - t1 + penalty

    flushBuffer()

    return elapsedTime

# A simple timing minigame which makes the player press space when a number is close to the target percentage. Speed changes how fast the number changes, effectively making the timing minigame harder the higher this value is. Returns how far off the player was from the number numerically.
def timingMinigame(targetPercentage = 50, speed = -3):
    currentValue = 0
    positive = True

    targetPercentage = min(100, max(targetPercentage, 0))
    speed = abs(speed)

    os.system("cls")
    print("Starting minigame, let go of space...")
    time.sleep(0.5)

    while not keyboard.is_pressed("space"):
        os.system("cls")
        print(f"Press space when the percentage is {targetPercentage}!")
        print(f"{currentValue}")

        currentValue = ((currentValue + speed) if positive else (currentValue - speed))

        if currentValue > 100:
            currentValue = 100
            positive = False
        
        elif currentValue < 0:
            currentValue = 0
            positive = True

        time.sleep(0.02)
    
    os.system("cls")
    flushBuffer()

    return abs(targetPercentage - currentValue)
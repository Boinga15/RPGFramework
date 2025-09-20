from framework.game import Game
from framework.enemy import Enemy
from framework.util import noLoopChoice

from typing import List
import os

class Battle:
    def __init__(self, game: Game, enemies: List[Enemy]):
        self.game = game
        self.enemies = enemies
    
    def doStep(self):
        shouldPause = False

        # Update party steps
        for character in self.game.party:
            if character.health <= 0:
                continue

            result = character.advanceStep(self.game, self)

            if result == 1:
                shouldPause = True

        # Update enemy steps
        for enemy in self.enemies:
            if enemy.health <= 0:
                continue

            result = enemy.advanceStep(self)

            if result == 1:
                shouldPause = True
        
        return shouldPause

    def startBattle(self):
        self.game.clearStory()

        doingBattle = True

        def checkForBattleEnds():
            enemyAlive = False
            
            for enemy in self.enemies:
                if enemy.health > 0:
                    enemyAlive = True
            
            if not enemyAlive:
                return 1 # All Enemies Killed

            playerAlive = False

            for character in self.game.party:
                if character.health > 0:
                    playerAlive = True
                    break
            
            if not playerAlive:
                return -1 # Entire party KOd.

            return 0 # No result yet.

        def updateDisplay():
            os.system("cls")

            # Step 1 - Console display (shift this to info or story if you wish to).
            print("==============================")
            for character in self.game.party:
                print(f"{character.name}:")

                if character.health <= 0:
                    print("K.O.")
                    print("-------------------------")
                    continue

                print(f"Health: {character.health} / {character.getMaxHealth()}")

                stepDisplay = ""
                currentDelay = (character.battleDelay[0] if character.battleDelay[0] > 0 else (character.battleDelay[1] if character.battleDelay[1] > 0 else character.battleDelay[2]))
                
                if currentDelay > 0:
                    stepDisplay = f"({currentDelay})"

                print(f"\nCurrent Action: {character.heldAction["display"]} {stepDisplay}")
                print("-------------------------\n")
            
            print("==============================")

            for enemy in self.enemies:
                print(f"{enemy.name}:")

                if enemy.health <= 0:
                    print("K.O.")
                    print("-------------------------")
                    continue

                print(f"Health: {enemy.health} / {enemy.getMaxHealth()}")

                stepDisplay = ""
                currentDelay = (enemy.battleDelay[0] if enemy.battleDelay[0] > 0 else (enemy.battleDelay[1] if enemy.battleDelay[1] > 0 else enemy.battleDelay[2]))
                
                if currentDelay > 0:
                    stepDisplay = f"({currentDelay})"

                print(f"\nCurrent Action: {enemy.heldAction["display"]} {stepDisplay}")
                print("-------------------------\n")


        def openCharacterActionMenu(character):
            isDone = False
            os.system("cls")

            while not isDone:
                updateDisplay()
                print("==============================")
                print(f"Current Character: {character.name}\n")
                
                choices = {}

                for choice in character.getBattleActions():
                    choices[choice] = choice
                
                resultId, result = noLoopChoice(choices)

                if result == None:
                    print("Invalid choice, please try again.\n")
                
                else:
                    actionResult = character.startAction(result, self.game, self)

                    if actionResult:
                        return


        while doingBattle:
            # Step 1 - Update the display.
            updateDisplay()

            # Step 2 - See if any characters have their action ready.
            readyCharId = -1

            for enemy in self.enemies:
                if enemy.battleDelay[0] + enemy.battleDelay[1] + enemy.battleDelay[2] <= 0:
                    enemy.chooseBattleAction()
            
            updateDisplay()

            for character in self.game.party:
                if character.battleDelay[0] + character.battleDelay[1] + character.battleDelay[2] <= 0 and character.health > 0:
                    openCharacterActionMenu(character)
                    updateDisplay()
            
            # Step 3 - Do the steps for characters and enemies.
            shouldPause = self.doStep()

            if shouldPause:
                updateDisplay()
                print("-------------------------")
                input("Press enter to continue...")
            
            # Step 4 - Check for end of battles.
            result = checkForBattleEnds()

            if result != 0:
                return result # End the battle. -1 = Party is down, 1 = All enemies defeated.
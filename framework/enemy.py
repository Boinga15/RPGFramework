from framework import Game

import random

class Enemy:
    def __init__(self, game: Game, name, health):
        self.game = game
        self.name = name

        self.maxHealth = health
        self.health = health

        self.battleDelay = [0, 0, 0] # Wind-up, Action, Wind-down
        self.heldAction = {
            "action": "NONE",
            "data": [],
            "display": "Waitnig"
        }

        self.inflictions = [] # Dictionary of type {"name": str, "level": int, "duration": int}
    
    def getMaxHealth(self):
        return self.maxHealth

    def changeHealth(self, amount: int, isAttack = False):
        changeAmount = amount

        self.health = min(self.getMaxHealth(), max(0, self.health + changeAmount))

        return changeAmount    

    # Responsible for printing out the initial description of the enemy. Best used to show the enemy's image.
    def initialBattleDescription(self):
        pass

    # Called when the enemy needs to decide what attack it should do.
    def chooseBattleAction(self):
        chosenAction = random.choice(["Attack", "Crush", "Heal"])

        self.heldAction = {
            "action": chosenAction,
            "data": [],
            "display": f"Winding Up {chosenAction}"
        }

        match chosenAction:
            case "Attack":
                self.battleDelay = [3, 0, 2]

            case "Crush":
                self.battleDelay = [8, 0, 5]


            case "Heal":
                self.battleDelay = [4, 0, 4]

    # Called whenever an enemy is doing an action during their action phase.
    def doingAction(self, action, battleInstance):
        pass
    
    # Called whenever an enemy starts doing an action, NOT when they select their list (that's chooseBattleAction).
    def onBeginAction(self, action, battleInstance):
        match action:
            case "Attack":
                chosenTarget = random.choice(self.game.party)
                changeAmount = chosenTarget.changeHealth(-3, True) * -1

                self.game.writeText(f"{self.name} dealt {changeAmount} to {chosenTarget.name}")


            case "Crush":
                chosenTarget = random.choice(self.game.party)
                changeAmount = chosenTarget.changeHealth(-10, True) * -1

                self.game.writeText(f"{self.name} dealt {changeAmount} to {chosenTarget.name}")


            case "Heal":
                self.game.writeText(f"{self.name} healed 5 HP.")
                self.changeHealth(5)

    # Called during battle in order to handle an infliction every tick.
    def handleInfliction(self, inflictionName, battleInstance):
        pass
    
    # Call to advance a step in combat.
    def advanceStep(self, battleInstance):
        returnValue = 0 # Return value. 0 = Nothing, 1 = Action Done (Pause Game)

        # Advance steps
        if self.battleDelay[0] > 0:
            self.heldAction["display"] = f"Winding Up {(self.heldAction["action"])}"
            self.battleDelay[0] -= 1
            
            if self.battleDelay[0] <= 0:
                self.onBeginAction(self.heldAction["action"], battleInstance)
                returnValue = 1
                
                self.heldAction["display"] = f"Doing {(self.heldAction["action"])}"
            
        elif self.battleDelay[1] > 0:
            self.heldAction["display"] = f"Doing {(self.heldAction["action"])}"
            self.battleDelay[1] -= 1

            if self.heldAction["type"] == "ITEM":
                self.heldAction["item_reference"].duiringBattleAction(self.heldAction["action"], battleInstance, self)
            
            else:
                self.doingAction(self.heldAction["action"], battleInstance)
            
            if self.battleDelay[1] <= 0:
                self.heldAction["display"] = "Winding Down"
        
        elif self.battleDelay[2] > 0:
            self.heldAction["display"] = "Winding Down"

            self.battleDelay[2] -= 1

            if self.battleDelay[2] <= 0:
                self.heldAction["display"] = "Waiting"
        
        # Tick down inflictions
        for infliction in self.inflictions:
            if infliction["duration"] > 0: # An infliction wtih -1 or lower is considered "infinite".
                infliction["duration"] -= 1
            
            self.handleInfliction(infliction["name"], battleInstance)
        
        cIndex = 0

        while cIndex < len(self.inflictions):
            if self.inflictions[cIndex]["duration"] == 0:
                self.inflictions.pop(cIndex)
            else:
                cIndex += 1
        
        return returnValue
    
    # Adds an infliction to the character. If upgradeInflictions is True, then adding the same infliction with a higher duration or level upgrades the existing infliction.
    def addInfliction(self, name: str, level: int = 1, duration: int = 10, upgradeInflictions = False):
        if upgradeInflictions:
            # Check inflictions.
            for infliction in self.inflictions:
                if infliction["name"] == name and (infliction["duration"] < duration or infliction["level"] < level):
                    infliction["duration"] = duration
                    infliction["level"] = level

                    return
            
            self.inflictions.append({
                "name": name,
                "duration": duration,
                "level": level
            })
    
    # Remove the first infliction from this character which matches with the name variable. Returns true if it successfully removed something, or false otherwise.
    def removeInfliction(self, name: str):
        for infliction in self.inflictions:
            if infliction["name"] == name:
                self.inflictions.remove(infliction)
                return True
        
        return False

class TestEnemy(Enemy):
    def __init__(self, game):
        super().__init__(game, "Test Enemy", 100)
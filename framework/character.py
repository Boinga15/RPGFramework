from typing import List
import os
import copy

from framework.util import noLoopChoice

class Character:
    def __init__(self, name: str = "", health: int = 100, carryCapacity: int = 10, baseBattleActions = ["Attack", "Block", "Dodge", "Use Item"]):
        self.name = name

        self.baseMaxHealth = health

        self.health = health
        self.inventory: List[item.Item] = []

        self.carryCapacity = carryCapacity

        self.baseBattleActions = baseBattleActions
        self.battleDelay = [0, 0, 0] # Wind-up, Action, Wind-down
        self.heldAction = {
            "type": "NONE",
            "item_reference": None,
            "action": "NONE",
            "data": [],
            "display": "Waitnig"
        }

        self.inflictions = [] # Dictionary of type {"name": str, "level": int, "duration": int}

    def getMaxHealth(self):
        return self.baseMaxHealth

    def changeHealth(self, amount: int, isAttack = False):
        changeAmount = amount

        if isAttack:
            if self.heldAction["action"] == "Dodge" and (self.battleDelay[1] > 0 and self.battleDelay[0] <= 0):
                changeAmount = 0
            
            elif self.heldAction["action"] == "Block" and (self.battleDelay[1] > 0 and self.battleDelay[0] <= 0):
                changeAmount *= 0.3

        self.health = min(self.getMaxHealth(), max(0, self.health + changeAmount))

        return changeAmount

    def getDamageMultiplier(self):
        return 1
    
    def getCurrentCarry(self):
        total = 0

        for item in self.inventory:
            total += item.carryCost
        
        return total

    def getMaxCarry(self):
        return self.carryCapacity

    def getBattleActions(self):
        actions = self.baseBattleActions

        return actions

    # Called whenever a battle begins. Useful to reset functions and values.
    def onBattleStart(self):
        self.battleDelay = [0, 0, 0]
        self.heldAction = {
            "type": "NONE",
            "item_reference": None,
            "action": "NONE",
            "data": [],
            "display": "Waiting"
        }
    
    # Called whenever a character is doing an action during their action phase.
    def doingAction(self, action, gameInstance, battleInstance):
        pass

    # Called whenever a character starts doing an action. NOT when an action of their's is selected.
    def onBeginAction(self, action, gameInstance, battleInstance):
        match action:
            case "Attack":
                damageDealt = self.heldAction["data"][0].changeHealth(-1 * self.getDamageMultiplier() * 3) * -1

                damageDealt = round(damageDealt * 100) / 100
                gameInstance.writeText(f"{self.name} attacked {self.heldAction["data"][0].name}, dealing {damageDealt} damage.")
            

            case "Block":
                gameInstance.writeText(f"{self.name} is now blocking.")
            

            case "Dodge":
                gameInstance.writeText(f"{self.name} moves to dodge.")
            

            case "Use Item":
                pass
    
    # Called whenever a character starts doing an action, so when it's selected from action list.
    def startAction(self, action, gameInstance, battleInstance):
        match action:
            case "Attack":
                isDone = False

                os.system("cls")
                while not isDone:
                    print("Select a target:")

                    choices = {}

                    for i, enemy in enumerate(battleInstance.enemies, start = 1):
                        choices[enemy.name + f" (Enemy #{i})"] = enemy
                    
                    choices["Back"] = "BACK"
                    
                    _, result = noLoopChoice(choices)
                    os.system("cls")

                    if result == None:
                        print("Invalid choice, please try again.")
                    
                    elif result == "BACK":
                        isDone = True
                    
                    else:
                        self.battleDelay = [3, 0, 2]
                        self.heldAction = {
                            "type": "CHARACTER",
                            "item_reference": None,
                            "action": "Attack",
                            "data": [result],
                            "display": "Winding Up Attack"
                        }

                        return True


            case "Block":
                self.battleDelay = [1, 5, 0]
                self.heldAction = {
                    "type": "CHARACTER",
                    "item_reference": None,
                    "action": "Block",
                    "data": [],
                    "display": "Winding Up Block"
                }

                return True
            

            case "Dodge":
                self.battleDelay = [3, 1, 1]
                self.heldAction = {
                    "type": "CHARACTER",
                    "item_reference": None,
                    "action": "Dodge",
                    "data": [],
                    "display": "Winding Up Dodge"
                }

                return True
            

            case "Use Item":
                os.system("cls")

                if len(self.inventory) <= 0:
                    print(f"{self.name} doesn't have any items to use.")
                    input("Press enter to continue...")

                isDone = False
                
                while not isDone:
                    print("Select an item to use:")

                    choices = {}

                    for i, item in enumerate(self.inventory, start = 1):
                        choices[f"{item.name} (Item #{i})"] = item
                    
                    choices["Back"] = "BACK"

                    _, result = noLoopChoice(choices)
                    os.system("cls")

                    if result == None:
                        print("Invalid choice, please try again.")
                    
                    elif result == "BACK":
                        isDone = True
                    
                    else:
                        isDone2 = False

                        while not isDone2:
                            print("Select an item to use:")

                            choices = {}

                            for action in item.getBattleActions(gameInstance):
                                choices[f"{action}"] = action
                            
                            choices["BACK"] = -1

                            _, result2 = noLoopChoice(choices)
                            os.system("cls")

                            if result2 == None:
                                print("Invalid choice, please try again.")
                            
                            elif result2 == -1:
                                isDone2 = True
                            
                            else:
                                finalResult = result.onActionSelect(result2, gameInstance, battleInstance, self)

                                if finalResult == True:
                                    return True


        return False # Assumed as an action failure.

    # Called during battle in order to handle an infliction every tick.
    def handleInfliction(self, inflictionName, gameInstance, battleInstance):
        pass
    
    # Call to advance a step in combat.
    def advanceStep(self, gameInstance, battleInstance):
        returnValue = 0 # Return value. 0 = Nothing, 1 = Action Done (Pause Game)

        # Advance steps
        if self.battleDelay[0] > 0:
            self.heldAction["display"] = f"Winding Up {(self.heldAction["action"])}"
            self.battleDelay[0] -= 1
            
            if self.battleDelay[0] <= 0:
                if self.heldAction["type"] == "ITEM":
                    self.heldAction["item_reference"].doBattleAction(self.heldAction["action"], gameInstance, battleInstance, self)
                    returnValue = 1
                
                else:
                    self.onBeginAction(self.heldAction["action"], gameInstance, battleInstance)
                    returnValue = 1
                
                self.heldAction["display"] = f"Doing {(self.heldAction["action"])}"
            
        elif self.battleDelay[1] > 0:
            self.heldAction["display"] = f"Doing {(self.heldAction["action"])}"
            self.battleDelay[1] -= 1

            if self.heldAction["type"] == "ITEM":
                self.heldAction["item_reference"].duiringBattleAction(self.heldAction["action"], gameInstance, battleInstance, self)
            
            else:
                self.doingAction(self.heldAction["action"], gameInstance, battleInstance)
            
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
            
            self.handleInfliction(infliction["name"], gameInstance, battleInstance)
        
        cIndex = 0

        while cIndex < len(self.inflictions):
            if self.inflictions[cIndex]["duration"] == 0:
                self.inflictions.pop(cIndex)
            else:
                cIndex += 1
        
        # Call item tick updates.
        for item in self.inventory:
            item.onBattleStep(gameInstance, battleInstance, self)
        
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

    # Adds items to the characters inventory, returning the number of items that the program failed to add.
    def addItem(self, itemToAdd, amount: int = 1):
        itemsAdded = 0

        while itemsAdded < amount:
            addedElement = False
            for item in self.inventory:
                if type(item) == type(itemToAdd) and item.quantity < item.maxQuantity:
                    item.quantity += 1
                    addedElement = True
                    break
            
            if not addedElement:
                if self.getCurrentCarry() + itemToAdd.carryCost > self.carryCapacity:
                    return amount - itemsAdded

                self.inventory.append(copy.deepcopy(itemToAdd))
            
            itemsAdded += 1
        
        return 0

    # Counts the number of items that are of a given class in this character's inventory.
    def countItems(self, itemClass):
        count = 0

        for item in self.inventory:
            if type(item) == itemClass:
                count += item.quantity
        
        return count

    # Removes a set number of items from the character's inventory, returning the number of items that couldn't be removed.
    def removeItems(self, itemClass, amount: int = 1):
        itemsToRemove = amount

        while itemsToRemove > 0:
            itemsToRemove -= 1
            
            cIndex = len(self.inventory) - 1

            while cIndex >= 0 and not (type(self.inventory[cIndex]) == itemClass):
                cIndex -= 1
            
            if cIndex == -1:
                return itemsToRemove + 1
            
            self.inventory[cIndex].quantity -= 1

            if self.inventory[cIndex].quantity <= 0:
                self.inventory.pop(cIndex)
        
        return 0


import framework.item as item
from typing import List

import copy

class Character:
    def __init__(self, name: str = "", health: int = 100, carryCapacity: int = 10):
        self.name = name

        self.baseMaxHealth = health

        self.health = health
        self.inventory: List[item.Item] = []

        self.carryCapacity = 10
    
    def getMaxHealth(self):
        return self.baseMaxHealth

    def changehealth(self, amount: int):
        self.health = min(self.getMaxHealth(), max(0, self.health + amount))

    def getCurrentCarry(self):
        total = 0

        for item in self.inventory:
            total += item.carryCost
        
        return total

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
                    return False

                self.inventory.append(copy.deepcopy(itemToAdd))
            
            itemsAdded += 1
        
        return True

    def countItems(self, itemClass):
        count = 0

        for item in self.inventory:
            if type(item) == itemClass:
                count += item.quantity
        
        return count

    def removeItems(self, itemClass, amount: int = 1):
        itemsToRemove = amount

        while itemsToRemove > 0:
            itemsToRemove -= 1
            
            cIndex = len(self.inventory) - 1

            while cIndex >= 0 and not (type(self.inventory[cIndex]) == itemClass):
                cIndex -= 1
            
            if cIndex == -1:
                return False
            
            self.inventory[cIndex].quantity -= 1

            if self.inventory[cIndex].quantity <= 0:
                self.inventory.pop(cIndex)


import framework.item as item
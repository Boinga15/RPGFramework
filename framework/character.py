from typing import List

import copy

class Character:
    def __init__(self, name: str = "", health: int = 100, carryCapacity: int = 10):
        self.name = name

        self.baseMaxHealth = health

        self.health = health
        self.inventory: List[item.Item] = []

        self.carryCapacity = carryCapacity
    
    def getMaxHealth(self):
        return self.baseMaxHealth

    def changehealth(self, amount: int):
        self.health = min(self.getMaxHealth(), max(0, self.health + amount))
    
    def getCurrentCarry(self):
        total = 0

        for item in self.inventory:
            total += item.carryCost
        
        return total

    def getMaxCarry(self):
        return self.carryCapacity

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
from framework import Item, Game, noLoopChoice

from typing import List
import os
import copy

# An object that contains several items. Can be stored in the Game class or in global storage for later use.
class Container:
    def __init__(self, game: Game, name: str = "Container", items: List[Item] = [], canTake: bool = True, canStore: bool = True, locked: bool = False, maxStorage = -1):
        self.game = game
        
        self.name = name
        self.items = items

        self.canTake = canTake
        self.canStore = canStore
        self.locked = locked
        self.maxStorage = maxStorage
    
    # Returns the current held capacity of the container.
    def getCurrentCarry(self):
        total = 0

        for item in self.items:
            total += item.carryCost
        
        return total

    def getMaxCarry(self):
        return self.maxStorage

    def _takeItems(self):
        while True:
            if not self.items:
                return

            print(f"Choose an item to take from {self.name}:")
            choices = {f"{i+1}: {it.name} (x{it.quantity})": it for i, it in enumerate(self.items)}
            choices["Back"] = "BACK"

            _, targetItem = noLoopChoice(choices, False)
            os.system("cls")

            if targetItem == "BACK":
                return

            elif targetItem == None:
                print("Invalid choice, please try again.\n")
                continue

            # Choose amount if >1
            max_amount = targetItem.quantity
            amount = 1
            if max_amount > 1:
                while True:
                    try:
                        amount = int(input(f"How many {targetItem.name} to take? (1 to {max_amount}, 0 = cancel): "))
                        os.system("cls")
                        if amount == 0:
                            return
                        if 1 <= amount <= max_amount:
                            break
                    except ValueError:
                        pass
                    os.system("cls")
                    print("Invalid number.\n")

            # Choose party member
            while True:
                print(f"Who should take the {targetItem.name}?")
                party_choices = {c.name: c for c in self.game.party}
                party_choices["Back"] = "BACK"

                _, targetChar = noLoopChoice(party_choices)
                os.system("cls")

                if targetChar == "BACK":
                    break

                # Transfer items one by one using deepcopy
                to_transfer = amount
                while to_transfer > 0:
                    newItem = copy.deepcopy(targetItem)
                    newItem.quantity = 1
                    failed = targetChar.addItem(newItem, 1)
                    if failed == 0:
                        targetItem.quantity -= 1
                        if targetItem.quantity <= 0:
                            self.items.remove(targetItem)
                            break
                    else:
                        print(f"{targetChar.name} cannot carry more of {targetItem.name}.")
                        input("Press Enter to continue.")
                        break
                    to_transfer -= 1

                break

    def _storeItems(self):
        while True:
            print("Whose inventory do you want to store from?")
            party_choices = {c.name: c for c in self.game.party}
            party_choices["Back"] = "BACK"

            _, targetChar = noLoopChoice(party_choices)
            os.system("cls")

            if targetChar == "BACK":
                return
            
            elif targetChar == None:
                print("Invalid choice, please try again.\n")
                continue

            if not targetChar.inventory:
                print(f"{targetChar.name} has no items.\n")
                continue

            # Choose item from character inventory
            while True:
                print(f"Choose an item from {targetChar.name}'s inventory:")
                choices = {f"{i+1}: {it.name} (x{it.quantity})": it for i, it in enumerate(targetChar.inventory)}
                choices["Back"] = "BACK"

                _, targetItem = noLoopChoice(choices, False)
                os.system("cls")

                if targetItem == "BACK":
                    break

                elif targetItem == None:
                    print("Invalid choice, please try again.\n")
                    continue

                # Choose amount if >1
                max_amount = targetItem.quantity
                amount = 1
                if max_amount > 1:
                    while True:
                        try:
                            amount = int(input(f"How many {targetItem.name} to store? (1-{max_amount}, 0=cancel): "))
                            if amount == 0:
                                return
                            if 1 <= amount <= max_amount:
                                break
                        except ValueError:
                            pass
                        print("Invalid number.")

                # Transfer loop
                to_transfer = amount
                while to_transfer > 0:
                    newItem = copy.deepcopy(targetItem)
                    newItem.quantity = 1
                    failed = self.addItem(newItem, 1)
                    if failed == 0:
                        targetItem.quantity -= 1
                        if targetItem.quantity <= 0:
                            targetChar.inventory.remove(targetItem)
                            break
                    else:
                        print(f"No space left in {self.name}.")
                        input("Press enter to continue...")
                        break
                    to_transfer -= 1
                break

    # Call to let the player interact with the container.
    def openContainer(self):
        if self.locked:
            os.system("cls")
            print(f'The container "{self.name}" is locked.')
            input("Press enter to continue...")
            return

        os.system("cls")
        isDone = False

        while not isDone:
            print(f"Items in container \"{self.name}\"")

            for i, item in enumerate(self.items, start = 1):
                print(f"{i}: {item.name} {f"({item.quantity} / {item.maxQuantity})" if item.quantity > 1 else ""}")
            
            choices = {}

            if self.canTake and len(self.items) > 0:
                choices["Take Items"] = "TAKE"
            
            if self.canStore and (self.maxStorage < 0 or self.getCurrentCarry() < self.maxStorage):
                choices["Store Items"] = "STORE"
            
            choices["Close"] = "CLOSE"

            print("\n=============================\n")

            _, result1 = noLoopChoice(choices)
            os.system("cls")


            if result1 == "TAKE":
                self._takeItems()
            

            elif result1 == "STORE":
                self._storeItems()
            

            elif result1 == "CLOSE":
                return
            

            else:
                print("Error: Invalid choice, please try again.")


    # Adds items to the container, returning the number of items that the program failed to add.
    def addItem(self, itemToAdd, amount: int = 1):
        itemsAdded = 0

        while itemsAdded < amount:
            addedElement = False
            for item in self.items:
                if type(item) == type(itemToAdd) and item.name == itemToAdd.name and item.quantity < item.maxQuantity:
                    item.quantity += 1
                    addedElement = True
                    break
            
            if not addedElement:
                if self.getCurrentCarry() + itemToAdd.carryCost > self.getMaxCarry():
                    return amount - itemsAdded

                self.items.append(copy.deepcopy(itemToAdd))
            
            itemsAdded += 1
        
        return 0

    # Counts the number of items that are of a given class in the container.
    def countItems(self, itemClass):
        count = 0

        for item in self.items:
            if type(item) == itemClass:
                count += item.quantity
        
        return count

    # Removes a set number of items from the container, returning the number of items that couldn't be removed.
    def removeItems(self, itemClass, amount: int = 1):
        itemsToRemove = amount

        while itemsToRemove > 0:
            itemsToRemove -= 1
            
            cIndex = len(self.items) - 1

            while cIndex >= 0 and not (type(self.items[cIndex]) == itemClass):
                cIndex -= 1
            
            if cIndex == -1:
                return itemsToRemove + 1
            
            self.items[cIndex].quantity -= 1

            if self.items[cIndex].quantity <= 0:
                self.items.pop(cIndex)
        
        return 0
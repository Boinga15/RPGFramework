import os
import copy

class Item:
    def __init__(self, name: str = "", description: str = "", carryCost: int = 1, maxQuantity: int = 1):
        self.name = name
        self.description = description

        self.carryCost = carryCost
        self.quantity = 1
        self.maxQuantity = maxQuantity

        self.standardActions = ["Give", "Discard"]
        self.battleActions = ["Give"]
    
    def doStandardAction(self, action: str, gameInstance, owningCharacter):
        match action:
            case "Give":
                os.system("cls")
                isDone = False

                # End early if there's only one character.
                if len(gameInstance.party) == 1:
                    print("There is only one person in the party.")
                    input("\nPress enter to continue...")
                    return
                
                while not isDone:
                    print("Select a character:")

                    cIndex = 1
                    for character in gameInstance.party:
                        print(f"{cIndex}: {character.name}")
                        cIndex += 1

                    print(f"{cIndex}: Cancel")

                    try:
                        charId = int(input("\n> "))
                        os.system("cls")

                        if not (0 < charId <= len(gameInstance.party) + 1):
                            print("Invalid input, please try again.\n")
                        elif charId == len(gameInstance.party) + 1:
                            return
                                       
                        elif gameInstance.party[charId - 1] == owningCharacter:
                            print("You cannot transfer items to the same person.\n")            

                        else:
                            isDone2 = False
                            targetCharacter = gameInstance.party[charId - 1]

                            while not isDone2:
                                print(f"{self.name} ({self.quantity} / {self.maxQuantity})\n")
                                print("Enter how much of this item you wish to transfer (enter 0 to cancel):")

                                try:
                                    amount = int(input("\n> "))
                                    os.system("cls")

                                    if amount < 0:
                                        print("Invalid input, please try again.")
                                    
                                    else:
                                        tempItem = copy.deepcopy(self)
                                        tempItem.quantity = 1

                                        quantityLeft = targetCharacter.addItem(tempItem, min(self.quantity, amount))
                                        self.quantity -= min(self.quantity, amount) - quantityLeft

                                        if self.quantity <= 0:
                                            owningCharacter.inventory.remove(self)

                                        return
                                
                                except ValueError:
                                    os.system("cls")
                                    print("Invalid input, please try again.")

                            return
                    
                    except ValueError:
                        os.system("cls")
                        print("Invalid input, please try again.")


            case "Discard":
                os.system("cls")

                isDone = False

                while not isDone:
                    print(f"{self.name} ({self.quantity} / {self.maxQuantity})\n")
                    print("Enter how much of this item you wish to discard (enter 0 to cancel):")

                    try:
                        amount = int(input("\n> "))
                        os.system("cls")

                        if amount < 0:
                            print("Invalid input, please try again.")
                        
                        else:
                            self.quantity -= amount

                            if self.quantity <= 0:
                                owningCharacter.inventory.remove(self)

                            isDone = True
                    
                    except ValueError:
                        os.system("cls")
                        print("Invalid input, please try again.")

    def doBattleAction(self, action: str, gameInstance, battleInstance, owningCharacter):
        pass

class TestItem(Item):
    def __init__(self):
        super().__init__("Test Item", "This is a test item.", 1, 5)
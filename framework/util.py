import os

# Pre-Implemented Functions
# Used to display auto-wrapping text on the console.
def neatPrint(inp: str, wrapLength: int = 80):
    pass

# Useful for displaying options to the player. "choices" should be a dictionary of type string --> any. Returns the selected choice's data.
def choice(choices, displayChoices = True):
    hasSelected = False
    
    os.system("cls")
    while not hasSelected:
        if displayChoices:
            for i, choice in enumerate(choices.keys(), start=1):
                print(f"{i}: {choice}")

            print("") 
        
        try:
            op = int(input("> "))
            os.system("cls")

            if op < 1 or op > len(choices):
                print("Error: Invalid input. Try again.\n")
            else:
                hasSelected = True
        
        except ValueError:
            os.system("cls")
            print("Error: Invalid input. Try again.\n")
    
    return choices[list(choices.keys())[op - 1]]

# Very similar to choice, however it auto-displays the choices and also doesn't loop.
def noLoopChoice(choices, showIndexes = True):
    for i, choice in enumerate(choices.keys(), start=1):
        if showIndexes:
            print(f"{i}: {choice}")
        else:
            print(f"{choice}")

    print("") 

    try:
        op = int(input("> "))

        if op < 1 or op > len(choices):
            return None, None
        else:
            return (op - 1), choices[list(choices.keys())[op - 1]]
    
    except ValueError:
        return None, None

os.system("cls")


# Allows for inventory management through dropping and gifting items.
def inventoryManagement(game):
    isDone = False

    while not isDone:
        print("=== INVENTORY MANAGEMENT ===")
        options = {}

        for character in game.party:
            options[character.name] = character.name
        
        options["Finish Inventory Management"] = -1

        charId, character = noLoopChoice(options)
        os.system("cls")

        if character == -1:
            isDone = True
        
        elif character == None:
            print("Error: Invalid choice, please try again.\n")
        
        else:
            isDone2 = False

            while not isDone2:
                print("=== INVENTORY MANAGEMENT ===")
                print(f"=== Chosen Character: {character} ({game.party[charId].getCurrentCarry()} / {game.party[charId].getMaxCarry()}) ===")

                options2 = {}

                for i, item in enumerate(game.party[charId].inventory):
                    options2[f"{i + 1}: {item.name} ({item.quantity} / {item.maxQuantity}) [Weight: {item.carryCost}]"] = item.name
                
                options2["Go Back"] = -1

                itemId, item = noLoopChoice(options2, False)
                os.system("cls")

                if item == -1:
                    isDone2 = True
                
                elif item == None:
                    print("Error: Invalid choice, please try again.\n")
                
                else:
                    isDone3 = False
                    itemRef = game.party[charId].inventory[itemId]

                    while not isDone3:
                        print("=== INVENTORY MANAGEMENT ===")
                        print(f"=== Chosen Character: {character} ===")
                        print(f"=== Chosen Item: {item} ===")
                        neatPrint(f"{itemRef.description}")

                        actionList = {}
                        

                        for action in itemRef.standardActions:
                            actionList[action] = action
                        
                        actionList["Go Back"] = -1

                        _, action = noLoopChoice(actionList)
                        os.system("cls")

                        if action == -1:
                            isDone3 = True
                        
                        elif action == None:
                            print("Error: Invalid choice, please try again.\n")
                        
                        else:
                            itemRef.doStandardAction(action, game, game.party[charId])
                            isDone3 = True

# Roman Numeral Conveter
def romanNumeralConversion(inputNumber: int):
    if inputNumber <= 0:
        return "0"

    outputString = ""
    
    conversionKeys = {
        "M": 1000,
        "D": 500,
        "C": 100,
        "L": 50,
        "X": 10,
        "V": 5,
        "I": 1
    }

    for key in conversionKeys.keys():
        requiredValue = conversionKeys[key]
        
        while inputNumber >= requiredValue:
            inputNumber -= requiredValue
            outputString += key
        
        # Check for any subtractions (e.g. IX).
        for otherKey in conversionKeys.keys():
            if conversionKeys[key] <= conversionKeys[otherKey]:
                continue
            
            finalValue = conversionKeys[key] - conversionKeys[otherKey]
            if finalValue <= inputNumber and finalValue != conversionKeys[otherKey]:
                outputString += f"{otherKey}{key}"
                inputNumber -= finalValue
    
    return outputString
class Item:
    def __init__(self, name: str = "", carryCost: int = 1, maxQuantity: int = 1):
        self.name = name

        self.carryCost = carryCost
        self.quantity = 1
        self.maxQuantity = maxQuantity

class TestItem(Item):
    def __init__(self):
        super().__init__("Test Item", 1, 5)
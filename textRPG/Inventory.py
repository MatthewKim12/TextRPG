class Inventory:
    def __init__(self, potions, armors, weapons):
        self.potions = potions
        self.armors = armors
        self.weapons = weapons
    def use_potion(self):
        if self.potions > 0:
            self.potions -= 1
            return True
        return False
    def add_potion(self):
        self.potions += 1
    def add_armor(self, defend):
        self.armors.append(defend)
    def add_weapon(self, attack):
        self.weapons.append(attack)
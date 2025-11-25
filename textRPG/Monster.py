import random
class Monster:
    def __init__(self, hp, attack, defend):
        self.hp = hp
        self.atk = attack
        self.defendhp = defend
    def damaged(self, amount):
        self.hp -= max(amount - random.randrange(self.defendhp[0], self.defendhp[1]), 0)
    def attack(self):
        return random.randrange(self.atk[0], self.atk[1])
    def is_defeated(self):
        return self.hp <= 0
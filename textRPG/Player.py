import random
class Player:
    def __init__(self, place, maxhp, hp, defend, attack):
        self.place = place
        self.maxhp = maxhp
        self.hp = hp
        self.defend = defend
        self.atk = attack
    def move(self, dx, dy):
        self.place = (self.place[0] + dx, self.place[1] + dy)
        self.recover(1)
    def damaged(self, amount):
        self.hp -= max(amount - random.randrange(self.defend[0], self.defend[1]), 0)
    def recover(self, amount):
        if self.hp + amount < self.maxhp:
            self.hp += amount
        else:
            self.hp = self.maxhp
    def attack(self):
        return random.randrange(self.atk[0], self.atk[1])
    def get_status(self):
        return self.hp
    def is_defeated(self):
        return self.hp <= 0
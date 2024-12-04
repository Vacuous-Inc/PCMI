from Card import Card
from random import choices

SUITS = ["s","h","c","d"]
RANKS = ["2","3","4","5","6","7","8","9","10",'J','Q','K','A']

class Deck:
    def __init__(self):
        self.deck = [Card(x+y) for y in SUITS for x in RANKS]

    def deal(self, num = 1):
        return choices(self.deck,k=num)
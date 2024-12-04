class Card:
    def __init__(self, card):
        self.suit = card[-1]
        self.rank = card[:-1]

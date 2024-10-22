'''
Main code for integrating different components and running the game itself
'''
#from Physical import Robot, Camera
import User


class Game:

    def __init__(self, players):
        self.players = players
        #self.dealer = Player()
        #self.robot = Robot()
        
    def start(self):
        #Robot.deal()
        for i, group in enumerate([1,2,]):#Camera.readDeal()):
            self.players[i].addCards(group)
        for p in self.players:
            if not p.blackjack:                
                p.take_turn()

    
    def resolve_board(self):
        for p in self.players:
            if p.blackjack:
                p.balance += p.wager * 2
            if not p.bust and (self.dealer.bust):
                pass

            elif p.bust or (p.handValue < self.dealer.handValue):
                pass
                
        



class Player:
    def __init__(user, self):
        self.user = user
        self.balance = user.balance
        self.hand = []
        self.handValue
        self.wager
        self.bust
        self.blackjack

    def take_turn(self):
        pass

    def blackjack():
        pass
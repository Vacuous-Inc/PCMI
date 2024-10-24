'''
Main code for integrating different components and running the game itself
'''
#from Physical import Robot, Camera
import User

global robot
robot = Robot()
global camera
camera = Camera()

class Game:

    def __init__(self, players):
        self.players = players
        self.dealer = Dealer()
        
        
    def start(self):
        robot.start()
        self.cardData = camera.readDeal()

        for i, p in self.players:
            p.addCards(self.cardData[2*i])
            p.addCards(self.cardData[(2*i)+1])
        
        for p in self.players:
            p.blackjack()
        
        self.dealer.addCards(self.cardData[-1])

        for i, p in self.players:
            p.take_turn(i)

        self.dealer.take_turn()

        self.resolve_board()

        dict = {
            "player_one": self.players[0].info,
            "player_two": self.players[1].info,
            "player_three": self.players[2].info,
            "dealer": self.dealer.info
        }
    
    def resolve_board(self):
        for p in self.players:
            if p.blackjack:
                p.balance += p.wager * 2
            elif not p.bust and (self.dealer.bust):
                p.balance += p.wager
            elif p.bust or (p.handValue < self.dealer.handValue):
                p.balance -= p.wager
                
        



class Player:
    def __init__(user, self):
        self.user = user
        self.balance = user.balance
        self.hand = []
        self.handValue
        self.wager
        self.bust
        self.blackjack

    def take_turn(self, place):
        while (not self.blackjack) and (not self.bust):
            #They take their turn??
            pass

    def hit(self, place):
        robot.deal(place)
        self.hand().append(camera.readDeal())
        #Add a value to the handValue but idk how to do that just yet
        self.blackjack()
        self.bust()
    
    def stand(self):
        #Lowkey not sure how to do this one either
        pass

    def double_down(self, place):
        self.wager *= 2
        robot.deal(place)
        self.hand().append(camera.readDeal())
        #Add a value to the handValue but idk how to do that just yet
        self.blackjack()
        self.bust()

    def blackjack():
        pass

    def bust():
        pass

    def info(self):
        dict = {
            "hand": self.hand,
            "value": self.handValue,
            "wager": self.wager,
            "bust": self.bust,
            "blackjack": self.blackjack
        }
        return dict

class Dealer:
    def __init__(self):
        self.hand = []
        self.handValue
        self.wager
        self.bust
        self.blackjack

    def take_turn(place, self):
        while sum(self.handValue) < 17:
            self.hit(place)
    
    def hit(place, self):
        robot.deal(place)
        self.hand().append(camera.readDeal())
        #Add a value to the handValue but idk how to do that just yet
        self.blackjack()
        self.bust()
    
    def stand(self):
        #Lowkey not sure how to do this one either
        pass

    def blackjack():
        pass

    def bust():
        pass

    def info(self):
        dict = {
            "hand": self.hand,
            "value": self.handValue,
            "wager": self.wager,
            "bust": self.bust,
            "blackjack": self.blackjack
        }
        return dict
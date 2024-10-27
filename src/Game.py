'''
Main code for integrating different components and running the game itself
'''
from Physical import Robot, Camera
from flask_socketio import emit

global robot
robot = Robot()
global camera
camera = Camera()

class Game:

    def __init__(self, players, namespace):
        self.players = [Player(x) for x in players]
        self.dealer = Dealer()
        self.space = namespace
        
        
    def start(self):
        robot.start()
        cardData = camera.readDeal()

        for i, p in enumerate(self.players):
            p.hand.append(cardData[2*i])
            p.handValue += parse_card(cardData[2*i])
            p.hand.append(cardData[(2*i)+1])
            p.handValue += parse_card(cardData[(2*i)+1])
        
        for p in self.players:
            p.blackjack()
        
        self.dealer.hand.append(cardData[-1])
        p.handValue += parse_card(cardData[-1])

        emit("Turn", {"Player":self.players[0].user.name, "Info":self.players[0].info()}, namespace=self.space)

    def dealer_turn(self):
        self.dealer.take_turn()
        self.resolve_board()
    
    def resolve_board(self):
        for p in self.players:
            if p.blackjack:
                p.balance += p.wager * 2
            elif (not p.bust) and (self.dealer.bust or (p.handValue > self.dealer.handValue)):
                p.balance += p.wager
            elif p.bust or (p.handValue < self.dealer.handValue):
                p.balance -= p.wager
            else:
                p.push = True
                pass

    def info(self):
        return {
            "player_one": self.players[0].info,
            "player_two": self.players[1].info,
            "player_three": self.players[2].info,
            "dealer": self.dealer.info
        }
                
FACES = ['K','Q','J']  

def parse_card(card):
    rank = card[0]

    if rank == 'A':
        return 11
    elif rank in FACES:
        return 10
    else:
        return rank



class Player:
    def __init__(self, user):
        self.user = user
        self.balance = user.balance
        self.hand = []
        self.handValue
        self.wager
        self.bust = False
        self.blackjack = False
        self.push = False

    '''
    def take_turn(self, place):
        while (not self.blackjack) and (not self.bust):
            #They take their turn??
            pass
    '''

    def hit(self, place):
        robot.deal(place)
        newCard = camera.readDeal()
        self.hand.append(newCard)
        self.handValue += parse_card(newCard)
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

    def blackjack(self):
        self.blackjack = self.handValue == 21

    def bust(self):
        self.bust = self.handValue > 21

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
        self.stand()
    
    def hit(place, self):
        robot.deal(place)
        newCard = camera.readDeal()
        self.hand.append(newCard)
        self.handValue += parse_card(newCard)
        #Add a value to the handValue but idk how to do that just yet
        self.blackjack()
        self.bust()
    
    def stand(self):
        #Lowkey not sure how to do this one either
        pass

    def blackjack(self):
        self.blackjack = self.handValue == 21

    def bust(self):
        self.bust = self.handValue > 21

    def info(self):
        dict = {
            "hand": self.hand,
            "value": self.handValue,
            "wager": self.wager,
            "bust": self.bust,
            "blackjack": self.blackjack
        }
        return dict
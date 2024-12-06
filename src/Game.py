'''
Main code for integrating different components and running the game itself
'''
from Physical import Robot
from flask_socketio import emit


global robot
robot = Robot()
global camera
camera = robot.camera



FACES = ['K','Q','J']  

def parse_card(card):
    rank = card.rank

    if rank == 'A':
        return 11
    elif rank in FACES:
        return 10
    else:
        return int(rank)


'''
Class for managing game flow
'''
class Game:

    def __init__(self, players, namespace):
        self.players = [Player(x) for x in players]
        self.dealer = Dealer()
        global space 
        space = namespace
        self.count = 0
        
    def start(self):
        robot.start(len(self.players))

        for i, p in enumerate(self.players):
            card1 = camera.getDealSpec(2*i)
            card2 = camera.getDealSpec((2*i)+1)
            p.hand.append(card1)
            p.handValue += parse_card(card1)
            p.hand.append(card2)
            p.handValue += parse_card(card2)
        
        for p in self.players:
            p.has_blackjack()
        
        card1 = camera.getDealSpec(-2)
        card2 = camera.getDealSpec(-1)
        self.dealer.hand.append(card1)
        self.dealer.handValue += parse_card(card1)
        self.dealer.hand.append(card2)
        self.dealer.handValue += parse_card(card2)

        emit("start", {"dealer":self.dealer.info()}, broadcast=True, namespace="/play")

        self.players[self.count].take_turn()

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

    def info(self):
        return {
            "player_one": self.players[0].info,
            "player_two": self.players[1].info,
            "player_three": self.players[2].info,
            "dealer": self.dealer.info
        }
    
    def advance(self):
        self.count += 1
        self.players[self.count].take_turn()
                
    def hit(self, player):
        p = self.players[self.count]
        if player == p.user.id:
            p.hit()



'''
Class for interfacing a player
'''
class Player:
    def __init__(self, user):
        self.user = user
        self.balance = user.balance
        self.hand = []
        self.handValue = 0
        self.wager = 0
        self.bust = False
        self.blackjack = False
        self.push = False

    
    def take_turn(self):
        if (not self.blackjack) and (not self.bust):
            print(f"{self.user.name}'s turn")
            emit("turn", {"Player":self.user.name, "Info":self.info()}, broadcast=True, namespace='/play')


    def hit(self, place):
        robot.deal(place)
        newCard = camera.get_deal(1)
        self.hand.append(newCard)
        self.handValue += parse_card(newCard)
        #Add a value to the handValue but idk how to do that just yet
        self.has_blackjack()
        self.has_bust()
    
    def stand(self):
        #Lowkey not sure how to do this one either
        pass

    def double_down(self, place):
        self.wager *= 2
        robot.deal(place)
        newCard = camera.get_deal(1)
        self.hand.append(newCard)
        self.handValue += parse_card(newCard)
        #Add a value to the handValue but idk how to do that just yet
        self.has_blackjack()
        self.has_bust()

    def has_blackjack(self):
        self.blackjack = self.handValue == 21

    def has_bust(self):
        self.bust = self.handValue > 21

    def info(self):
        dict = {
            "hand": [[x.rank, x.suit] for x in self.hand],
            "value": self.handValue,
            "wager": self.wager,
            "bust": self.bust,
            "blackjack": self.blackjack
        }
        return dict


'''
Class for controlling the dealer
'''
class Dealer:
    def __init__(self):
        self.hand = []
        self.handValue = 0
        self.wager = 0
        self.bust = False
        self.blackjack = False

    def take_turn(place, self):
        while sum(self.handValue) < 17:
            self.hit(place)
        self.stand()
    
    def hit(place, self):
        robot.deal(place)
        newCard = camera.get_deal(1)
        self.hand.append(newCard)
        self.handValue += parse_card(newCard)
        #Add a value to the handValue but idk how to do that just yet
        self.has_blackjack()
        self.has_bust()
    
    def stand(self):
        #Lowkey not sure how to do this one either
        pass

    def has_blackjack(self):
        self.blackjack = self.handValue == 21

    def has_bust(self):
        self.bust = self.handValue > 21

    def info(self):
        dict = {
            "hand": [[x.rank, x.suit] for x in self.hand],
            "value": self.handValue,
            "wager": self.wager,
            "bust": self.bust,
            "blackjack": self.blackjack
        }
        return dict
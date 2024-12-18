'''
Class for interacting with the robotic arm, pumps, and camera
'''

from math import sqrt, atan
import RPi.GPIO as GPIO
#from RPiSim.GPIO import GPIO
import time
import requests
from Constants import CameraIP

from Deck import Deck
from Card import Card


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#TODO Tune values, fill in some code, unify coordinate system

class Robot:
    def __init__(self):

        #pin definitions
        self.basePin = 6
        self.shoulderPin = 13
        self.elbowPin = 19
        self.wristPin = 26

        #declare pins as output
        [GPIO.setup(x, GPIO.OUT) for x in [self.basePin, self.shoulderPin, self.elbowPin, self.wristPin]]

        #declare pins as PWM
        self.base = GPIO.PWM(self.basePin, 50)
        self.shoulder = GPIO.PWM(self.shoulderPin, 50)
        self.elbow = GPIO.PWM(self.elbowPin, 50)
        self.wrist = GPIO.PWM(self.wristPin, 50)

        #start PWM and set angle to 0
        self.base.start(5.4)
        self.shoulder.start(6)
        self.elbow.start(2)
        self.wrist.start(7)

        self.baseTheta = 0
        self.shoulderTheta = 0
        self.elbowTheta = 0
        self.wristTheta = 0

        #get our pump
        self.pump = Pump()

        GPIO.setup(2, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)

        #get our camera
        self.camera = Camera()

        #testing values
        self.deck = Deck()


    def start(self, numPlayers):
        print(f"players: {numPlayers}")
        for i in range((numPlayers*2) + 2):
            self.deal(i%numPlayers)
        #print(f"dealing initial cards{self.camera.get_deal(2)}")

    #moves arm to specified distance
    def extend(self, r):

        if r == "p":
            self.wrist.start(7)
            time.sleep(0.5)
            self.elbow.start(2)
            self.shoulder.start(5.5)
        elif r == "d":
            self.wrist.start(7.15)
            time.sleep(0.5)
            self.shoulder.start(4.5)
            self.elbow.start(5.3)
        elif r == "c":
            self.shoulder.start(8.5)
            self.elbow.start(8)
            self.wrist.start(12)
            self.shoulder.start(7.75)


    #rotates arm to specified angle
    def rotate(theta,self):
        if theta == 0:
            self.base.start(5.4)
        elif theta == 1:
            self.base.start(3.7)
        elif theta == 2:
            self.base.start(5.4)  
        elif theta == 3:
            self.base.start(7)   
    
    #moves hand to specied point
    def move_to_coords(x,y,self):
        self.extend(sqrt(x**2 + y**2))
        self.rotate(atan(y/x))

    #moves a card from specified point to specified point
    def move_card(x1,y1,x2,y2,self):
        self.move_to_coords(x1,y1)
        self.pump.pickup()

        self.move_to_coords(x2,y2)
        self.pump.release()

    #deals a card to correct location
    def deal(self,pos):
        self.extend("c")
        print("extended")
        time.sleep(5)
        print("pump on")
        #self.pump.pickup()
        GPIO.output(2, GPIO.HIGH)
        GPIO.output(4, GPIO.HIGH)
        time.sleep(5)
        print("showing camera")
        self.elbow.start(6)
        self.shoulder.start(7)
        self.wrist.start(5)
        #self.camera.read_deal(self.deck)
        time.sleep(3)
        print(f"Dealt 1 card to {pos}")
        self.shoulder.start(8.2)
        time.sleep(0.5)
        self.rotate(pos)
        if pos:
            self.extend("p")
        else:
            self.extend("d")
        self.pump.release()
        '''
        self.camera.read_deal(self.deck)
        '''
        


#control the vaccuum punp
class Pump:
    def __innit__(self):
        self.pumpPins = 2
        self.valvePin = 4

        GPIO.setup(2, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)
    
    def pickup(self):
        GPIO.output(4, GPIO.HIGH)
        GPIO.output(2, GPIO.HIGH)
        

    def release(self):
        GPIO.output(4, GPIO.LOW)
        GPIO.output(2, GPIO.LOW)



#Class for handling card recoginition and camera i/o
class Camera:
    def __init__(self):
        self.read = set()
        self.queue = []
        self.cameraIP = CameraIP()

    def get_deal(self, x):
        
        hold = []
        if self.queue:
            for _ in range(x):
                hold.append(self.queue.pop(0))
        return hold

    def getDealSpec(self,x): 
        if self.queue:
            return self.queue.pop(x)
        return []
        
    def read_deal(self,deck):
        '''
        cards = requests.get(self.cameraIP).json()["Cards"]
        for c in cards:
            print(c)
            if c not in self.read:
                self.read.add(c)
                self.queue.append(Card(c))

        '''
        deal = deck.deal(1)
        self.queue.extend(deal)
        
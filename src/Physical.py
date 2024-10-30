'''
Class for interacting with the robotic arm and card shuffler
'''

from math import sqrt, atan, acos
#import RPi.GPIO as GPIO
from RPiSim.GPIO import GPIO
import time

from Deck import Deck


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#TODO Tune values, fill in some code, unify coordinate system

class Robot:
    def __init__(self):

        #variables to store current position - not currently used
        self.baseRotation = 0
        self.armPosition = 0

        #total distance from base to player
        self.totalLength = 3

        #pin definitions
        self.basePin = 15
        self.waistPin = 13
        self.shoulderPin = 11
        self.elbowPin = 14
        self.wristPin = 16

        #declare pins as output
        #GPIO.setup([self.basePin, self.waistPin, self.shoulderPin, self.elbowPin, self.wristPin], GPIO.OUT)
        [GPIO.setup(x, GPIO.OUT) for x in [self.basePin, self.waistPin, self.shoulderPin, self.elbowPin, self.wristPin]]

        #declare pins as PWM
        self.base = GPIO.PWM(self.basePin, 50)
        self.waist = GPIO.PWM(self.waistPin, 50)
        self.shoulder = GPIO.PWM(self.shoulderPin, 50)
        self.elbow = GPIO.PWM(self.elbowPin, 50)
        self.wrist = GPIO.PWM(self.wristPin, 50)

        #start PWM and set angle to 0
        #self.base.start(0)
        #self.waist.start(0)
        #self.shoulder.start(0)
        #self.elbow.start(0)
        #self.wrist.start(0)

        #get our shuffler
        self.shuffler = Shuffler()

        #get our pump
        self.pump = Pump()

        #get our camera
        self.camera = Camera()


        #testing values
        self.deck = Deck()


    def start(self, numPlayers):
        print(numPlayers)
        deal = self.deck.deal((numPlayers*2) + 1)
        print(deal)
        self.camera.queue.extend(deal)
        print("dealing initial cards")

    #moves arm to specified distance
    def extend(r,self):
        theta = acos(r/self.totalLength)

        dc = (theta/36) + 5
        dc_ = ((90-theta)/36) + 5
        
        #self.waist.ChangeDutyCycle(dc)
        #self.shoulder.ChangeDutyCycle(dc*2)
        #self.elbow.ChangeDutyCycle(dc_)

    #rotates arm to specified angle
    def rotate(theta,self):
        dc = (theta/36) + 5
        #self.base.ChangeDutyCycle(dc)

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

    #wrap the shuffler
    def shuffle(self):
        self.shuffler.shuffle()

    def deal(self,pos):
        self.camera.queue.extend(self.deck.deal(1))
        print(f"Dealt 1 card to {pos}")

#control the shuffler
class Shuffler:
    def __innit__(self):

        #set up pins and output
        self.shufflerPin = 18

        GPIO.setup(self.shufflerPin, GPIO.OUT)

    #performs one full shuffler
    def shuffle(self):
        #TODO write real code
        GPIO.output(self.shufflerPin, GPIO.HIGH)

#control the vaccuum punp
class Pump:
    def __innit__(self):
        self.pumpPin = 3
        self.valvePin = 5

        GPIO.setup(self.pumpPin, GPIO.OUT)
        GPIO.setup(self.valvePin, GPIO.OUT)
    
    def pickup(self):
        #TODO tune sleep values
        GPIO.output(self.pumpPin, GPIO.HIGH)
        GPIO.output(self.valvePin, GPIO.LOW)
        time.sleep(2)
        GPIO.output(self.pumpPin, GPIO.LOW)
        

    def release(self):
        GPIO.output(self.valvePin, GPIO.HIGH)



#Class for handling card recoginition and camera i/o
class Camera:
    def __init__(self):
        self.queue = []
        pass

    def read_deal(self):
        hold = self.queue
        print(hold)
        self.queue = []
        print(hold)
        return hold
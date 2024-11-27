'''
Class for interacting with the robotic arm and card shuffler
'''

from math import sqrt, atan, acos, cos, sin
#import RPi.GPIO as GPIO
from RPiSim.GPIO import GPIO
import time
import requests

from Deck import Deck


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
        #self.base.start(2)
        #elf.shoulder.start(2)
        #self.elbow.start(2)
        #self.wrist.start(2)

        self.baseTheta = 0
        self.shoulderTheta = 0
        self.elbowTheta = 0
        self.wristTheta = 0

        #get our pump
        self.pump = Pump()

        #get our camera
        self.camera = Camera()

        #testing values
        self.deck = Deck()


    def start(self, numPlayers):
        print(f"players: {numPlayers}")
        for i in range((numPlayers*2) + 2):
            self.camera.read_deal(self.deck)
        print("dealing initial cards")

    #moves arm to specified distance
    def extend(r, self):

        tolerance = 0.01

        #angle constants
        yPosition = 5
        psi = -90

        #lengths of components
        shoulderLength = 435
        forearmLength = 425
        
        #initializing angles
        theta1 = atan(yPosition/r) - atan((forearmLength*sin(theta2))/(shoulderLength + forearmLength*cos(theta2)))
        theta2 = 180 - (acos((r^2 + yPosition^2 - (shoulderLength)^2 - (forearmLength)^2)/(2*shoulderLength*forearmLength)))
        theta3 = 180 - (psi - theta1 - theta2)

        offset = self.shoulderTheta - theta1
        while abs(offset) > tolerance:
            dc1 = ((self.shoulderTheta-(offset/100))/18) + 2
            offset -= offset/100
            self.shoulder.ChangeDutyCycle(dc1)
            time.sleep(0.01)

        
        offset = self.elbowTheta - theta2
        while abs(offset) > tolerance:
            dc1 = ((self.elbowTheta-(offset/100))/18) + 2
            offset -= offset/100
            self.elbow.ChangeDutyCycle(dc1)
            time.sleep(0.01)

        
        offset = self.wristTheta - theta3
        while abs(offset) > tolerance:
            dc1 = ((self.wristTheta-(offset/100))/18) + 2
            offset -= offset/100
            self.wrist.ChangeDutyCycle(dc1)
            time.sleep(0.01)

    #rotates arm to specified angle
    def rotate(theta,self):
        tolerance = 0.01

        offset = self.baseTheta - theta
        while abs(offset) > tolerance:
            dc1 = ((self.baseTheta-(offset/100))/20) + 2
            offset -= offset/100
            self.base.ChangeDutyCycle(dc1)
            time.sleep(0.01)

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

    def deal(self,pos):
        self.camera.read_deal(self.deck)
        print(f"Dealt 1 card to {pos}")


#control the vaccuum punp
class Pump:
    def __innit__(self):
        self.pumpPins = [2,3]
        self.valvePin = 4

        GPIO.setup(self.pumpPins, GPIO.OUT)
        GPIO.setup(self.valvePin, GPIO.OUT)
    
    def pickup(self):
        #TODO tune sleep values
        GPIO.output(self.valvePin, GPIO.HIGH)
        GPIO.output(self.pumpPins, GPIO.HIGH)
        

    def release(self):
        GPIO.output(self.valvePin, GPIO.LOW)
        GPIO.outpit(self.pumpPins, GPIO.LOW)



#Class for handling card recoginition and camera i/o
class Camera:
    def __init__(self):
        self.read = {}
        self.queue = []
        self.cameraIP = "10.245.222.203:5000/data"

    def get_deal(self, x):
        hold = []
        for _ in range(x):
            hold.append = self.queue.pop(0)
        return hold

    def getDealSpec(self,x): 
        return self.queue.pop(x)
        
    def read_deal(self,deck):
        '''
        try:
            cards = requests.get(self.cameraIP).json()["Cards"]
            for c in cards:
                if c not in self.read:
                    self.read.add(c)
                    self.queue.append(c)
        except:
            print("ERROR")
        '''
        deal = deck.deal(1)
        self.queue.extend(deal)
'''
Class for interacting with the robotic arm and card shuffler
'''

from math import sqrt, arctan
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Robot:
    def __init__(self):

        #variables to store current position - not currently used
        self.baseRotation = 0
        self.armPosition = 0

        #pin definitions
        self.basePin = 15
        self.waistPin = 13
        self.shoulderPin = 11
        self.elbowPin = 14
        self.wristPin = 16

        #declare pins as output
        GPIO.setup([self.basePin, self.waistPin, self.shoulderPin, self.elbowPin, self.wristPin], GPIO.OUT)

        #declare pins as PWM
        self.base = GPIO.PWM(self.basePin, 60)
        self.waist = GPIO.PWM(self.waistPin, 60)
        self.shoulder = GPIO.PWM(self.shoulderPin, 60)
        self.elbow = GPIO.PWM(self.elbowPin, 60)
        self.wrist = GPIO.PWM(self.wristPin, 60)

        #start PWM and set angle to 0
        self.base.start(0)
        self.waist.start(0)
        self.shoulder.start(0)
        self.elbow.start(0)
        self.wrist.start(0)

        #get our shuffler
        self.shuffler = Shuffler()

    #moves arm to specified distance
    def extend(r,self):
        self.waist.ChangeDutyCycle()

    #rotates arm to specified angle
    def rotate(theta,self):
        self.base.ChangeDutyCycle()

    #moves hand to specied point
    def move_to_coords(x,y,self):
        self.extend(sqrt(x**2 + y**2))
        self.rotate(arctan(y/x))

    #wrap the shuffler
    def shuffle(self):
        self.shuffler.shuffle()


#control the shuffler
class Shuffler:
    def __innit__(self):

        #set up pins and output
        self.shufflerPin = 18

        GPIO.setup(self.shufflerPin, GPIO.OUT)

    #performs one full shuffler
    def shuffle(self):
        GPIO.output(self.shufflerPin, GPIO.HIGH)
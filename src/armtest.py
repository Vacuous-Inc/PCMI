import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pins = [6,13,19,26]
GPIO.setup(pins, GPIO.OUT)

servos = [GPIO.PWM(x,50) for x in pins]

[x.start(7) for x in servos]

while True:
    try:
        pin = int(input("servo#: "))
        rot = float(input("rot: "))

        servos[pin].ChangeDutyCycle(rot)
    except:
        GPIO.cleanup()
        exit()
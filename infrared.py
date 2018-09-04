# infrared
import RPi.GPIO as GPIO
import time
from servoMovement import *


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

print("warming up")
time.sleep(2)



GPIO.setwarnings(False)

GPIO.setup(2,GPIO.OUT) #PIN 2 -> Red LED as output
GPIO.setup(3,GPIO.OUT) #PIN 3 -> Green LED as output
GPIO.setup(14,GPIO.IN) #PIN 14 -> IR sensor as input




def infraredmain():
    
    status = 0
    while True:
                
        # Set the angle cycle (between 0 and 180)
        rest()
        print("GPIO.input(14) =", GPIO.input(14))
        print("status =", status)
                
        if(GPIO.input(14)==0) and status == 0:
            # no hand detected and not moving, stay at rest
            GPIO.output(2,True)
            GPIO.output(3,False)
            status = 0
            time.sleep(0.5)
        elif (GPIO.input(14)==1) and status == 0:
            # hand detected and not moving, move up
            GPIO.output(3,True) 
            GPIO.output(2,False) 
            up()
            time.sleep(0.5)
            status = 1
        elif (GPIO.input(14)==0) and status == 1:
            # no hand detected and moving up, move to resting state
            GPIO.output(2,True)
            GPIO.output(3,False)
            rest()
            status = 0
            time.sleep(0.5)
        elif (GPIO.input(14) == 1) and status == 1:
            # hand detected and moving up, move down
            GPIO.output(3,True)
            GPIO.output(2,False)
            down()
            time.sleep(0.5)
            status = 2
        elif (GPIO.input(14) == 0) and status == 2:
            # no hand detected and moving down, move to resting
            rest()
            status = 0
            time.sleep(0.5)
        elif (GPIO.input(14) == 1) and status == 2:
            # hand detected and moving down, move up
            GPIO.output(3,True)
            GPIO.output(2,False)
            up()
            time.sleep(0.5)
            status = 1
                    

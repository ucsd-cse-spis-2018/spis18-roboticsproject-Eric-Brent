# Libraries
import RPi.GPIO as GPIO
import time
 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# set GPIO Pins
GPIO_Servo = 4

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Servo, GPIO.OUT)



# Set PWM parameters
pwm_frequency = 50
duty_min = 2.5 * float(pwm_frequency) / 50.0
duty_max = 12.5 * float(pwm_frequency) / 50.0


# Set the duty cycle
def set_duty_cycle(angle):
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)

    
# Create a PWM instance
pwm_servo = GPIO.PWM(GPIO_Servo, pwm_frequency//2)

# Set the angle cycle (between 0 and 180)
angle = 90
#pwm_servo.start(set_duty_cycle(angle))

def right():
    angle = 0
    pwm_servo.start(set_duty_cycle(angle))
    #print("right")
def left():
    angle = 20
    pwm_servo.start(set_duty_cycle(angle))
    #print("left")
def middle():
    pwm_servo.start(0)
    #print("middle")
 
# Main program 
##if __name__ == '__main__':
##    try:
##        while True:
##        print(np)
##            middle()
##            print ("0")
##            time.sleep(1)
            
            

            
    # Reset by pressing CTRL + C
##    except KeyboardInterrupt:
##        print("Program stopped by User")
##        GPIO.cleanup()

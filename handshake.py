# Servo libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_Servo = 17

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
pwm_servo = GPIO.PWM(GPIO_Servo, pwm_frequency)

def up():
    angle = 0
    pwm_servo.start(set_duty_cycle(angle))


def rest():
    angle = 40
    pwm_servo.start(set_duty_cycle(angle))


def down():
    angle = 80
    pwm_servo.start(set_duty_cycle(angle))

def shake():
    up()
    time.sleep(0.5)
    down()
    time.sleep(0.5)

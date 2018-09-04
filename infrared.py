# servo
import RPi.GPIO as GPIO
import time


# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)


# Libraries
import Adafruit_MCP3008

# Software SPI
# The library interface uses BCM labeling
# Connect the chip to the following pins
#       CLK to GPIO 18 (physical pin 12)
#       MISO to GPIO 23 (physical pin 16)
#       MOSI to GPIO 24 (physical pin 18)
#       CS to GPIO 25 (physical pin 22) 
mcp = Adafruit_MCP3008.MCP3008(clk=12,cs=22,miso=16,mosi=18)
 
# set GPIO Pins
GPIO_Servo = 11

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




print("warming up")
time.sleep(2)


# infrared
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setup(3,GPIO.OUT) #PIN 3 -> Red LED as output
GPIO.setup(5,GPIO.OUT) #PIN 5 -> Green LED as output
GPIO.setup(8,GPIO.IN) #PIN 8 -> IR sensor as input





print("Reading values")

if __name__ == '__main__':
    try:
        status = 0
        while True:
            values = [0]*8
            for i in range(8):
                values[i] = mcp.read_adc(i)

            print(' | {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
            time.sleep(0.5)

            
            # Set the angle cycle (between 0 and 180)
            angle = 150
            pwm_servo.start(set_duty_cycle(angle))
            print("GPIO.input(8) =", GPIO.input(8))
            print("status =", status)
            
            if(GPIO.input(8)==0) and status == 0:
                # no hand detected and not moving, stay at rest
                GPIO.output(3,True)
                GPIO.output(5,False)
                status = 0
                time.sleep(0.5)
            elif (GPIO.input(8)==1) and status == 0:
                # hand detected and not moving, move up
                GPIO.output(5,True) 
                GPIO.output(3,False) 
                angle = 120
                pwm_servo.start(set_duty_cycle(angle))
                time.sleep(0.5)
                status = 1
            elif (GPIO.input(8)==0) and status == 1:
                # no hand detected and moving up, move to resting state
                GPIO.output(3,True)
                GPIO.output(5,False)
                angle = 150
                pwm_servo.start(set_duty_cycle(angle))
                status = 0
                time.sleep(0.5)
            elif (GPIO.input(8) == 1) and status == 1:
                # hand detected and moving up, move down
                GPIO.output(5,True)
                GPIO.output(3,False)
                angle = 180
                pwm_servo.start(set_duty_cycle(angle))
                time.sleep(0.5)
                status = 2
            elif (GPIO.input(8) == 0) and status == 2:
                # no hand detected and moving down, move to resting
                angle = 150
                pwm_servo.start(set_duty_cycle(angle))
                status = 0
                time.sleep(0.5)
            elif (GPIO.input(8) == 1) and status == 2:
                # hand detected and moving down, move up
                GPIO.output(5,True)
                GPIO.output(3,False)
                angle = 120
                pwm_servo.start(set_duty_cycle(angle))
                time.sleep(0.5)
                status = 1
                

    except KeyboardInterrupt:
        print("Program stopped by User")
        GPIO.cleanup()

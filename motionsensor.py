# Libraries
import RPi.GPIO as GPIO
import time
 
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
# set GPIO Pins
GPIO_Servo = 7

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Servo, GPIO.OUT)






# This program demonstrates how to control an ultrasound distance sensor

# Import the relevant libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
# set GPIO Pins
TriggerPin  = 12
EchoPin     = 18
 
# set GPIO direction (IN / OUT)
GPIO.setup(TriggerPin, GPIO.OUT)
GPIO.setup(EchoPin, GPIO.IN)








# Set PWM parameters
pwm_frequency = 50
duty_min = 2.5 * float(pwm_frequency) / 50.0
duty_max = 12.5 * float(pwm_frequency) / 50.0

# Set the duty cycle
def set_duty_cycle(angle):
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)

# Create a PWM instance
pwm_servo = GPIO.PWM(GPIO_Servo, pwm_frequency)






# Wait for sensor to settle
GPIO.output(TriggerPin, False)
print("Waiting for sensor to settle")
time.sleep(2)
print("Start sensing")

# Helper function to get the distance from the ultrasound sensor.
# It returns the measured distance in cm or -1 if it doesn't detect anything nearby.
# The function can take up to 0.25 seconds to execute.
# The details are not important; you should not modify this code
# --- Start of the ultrasound sensor helper function ---
def distance():
    
    # Create a pulse on the trigger pin
    # This activates the sensor and tells it to send out an ultrasound signal
    GPIO.output(TriggerPin, True)
    time.sleep(0.00001)
    GPIO.output(TriggerPin, False)

    # Wait for a pulse to start on the echo pin
    # The response is not valid if it takes too long, and we should break the loop
    valid = True
    RefTime = time.time()
    StartTime = RefTime
    while (GPIO.input(EchoPin) == 0) and (StartTime-RefTime < 0.1):
        StartTime = time.time()
    if (StartTime-RefTime >= 0.1):
        valid = False
        
    # Wait for a pulse to end on the echo pin
    # The response is not valid if it takes too long, and we should break the loop
    if (valid):
        RefTime = time.time()
        StopTime = time.time()
        while (GPIO.input(EchoPin) == 1) and (StopTime-RefTime < 0.1):
            StopTime = time.time()
        if (StopTime-RefTime >= 0.1):
            valid = False
        
    # If we received a complete pulse on the echo pin (i.e., valid == True)
    # Calculate the distance based on the length of the echo pulse and
    # the speed of sound (34300 cm/s)
    if (valid):
        EchoPulseLength = StopTime - StartTime
        return (EchoPulseLength * 34300) / 2        # Divide by 2 because we are calculating based on a reflection, so the travel time there and back
    else:
        return -1
        
# --- End of the ultrasound sensor helper function ---





# Set the angle cycle (between 0 and 180)
angle = 140
pwm_servo.start(set_duty_cycle(angle))

# Main program 
if __name__ == '__main__':
    try:
         
        
        while True:
            dist = distance()
            print(dist)
            time.sleep(0.10)
            if dist <= 5:
                time.sleep(0.25)
                angle = 180
                pwm_servo.start(set_duty_cycle(angle))
                print ("180")
                time.sleep(0.50)
                angle = 140
                pwm_servo.start(set_duty_cycle(angle))
                print ("120")
                time.sleep(0.25)
            
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Program stopped by User")
        GPIO.cleanup()


    

"""Class controlling the shield servo"""

from machine import Pin, PWM
from time import sleep

SERVO_PIN = PWM(Pin(16))
SERVO_PIN.freq(50)
#SERVO_PIN.duty_ns(9000) 

servoRange = int(40)
minServoAngle = int(90 - (servoRange//2)) # i.e max shield angle (full moon)
maxServoAngle = int(90 + (servoRange//2)) # i.e min shield angle (full moon)

# set max and min duty
maxDuty = int(9000)
minDuty = int(1000)

offset = 2.25
offsetDuty = int(minDuty+(maxDuty-minDuty)*(offset/180))

class Servo():

    def __init__(self):
        
        mid_position_duty = int(minDuty+(maxDuty-minDuty)*(90/180)) - offsetDuty
        SERVO_PIN.duty_u16(mid_position_duty)

    

    def setAngle(self, degrees):
        print("Setting angle to:", degrees, "degrees")
        duty = int(minDuty+(maxDuty-minDuty)*(degrees/180)) - offsetDuty
        SERVO_PIN.duty_u16(duty)
        sleep(1)
        SERVO_PIN.duty_u16(0)
        

    
    def trackToPosition(self, current_degrees, new_degrees):
        """Track slowly to position. Called on startup and as part of reset procedure"""

    
        current_duty = int(minDuty+(maxDuty-minDuty)*(current_degrees/180)) - offsetDuty
        new_duty = int(minDuty+(maxDuty-minDuty)*(new_degrees/180)) - offsetDuty
        
        if current_duty < new_duty:
            for i in range(current_duty, new_duty, 1):
                SERVO_PIN.duty_u16(i)
                sleep(0.004)
        else:
            for i in range(current_duty, new_duty, -1):
                SERVO_PIN.duty_u16(i)
                sleep(0.004)

        SERVO_PIN.duty_u16(int(0)) # deactivate 
        sleep(1)
          


    def tickTock(self, current_degrees, new_degrees, trackToStart):
        """Tick to next shield position. Assumes step is small as fast motion."""


        if trackToStart:
            print("Tracking to start ..")
            self.trackToPosition(current_degrees, new_degrees)

        else:

            print("Setting angle to:", new_degrees, "degrees")
            
            # Calcuate and set servo position
            duty = int(minDuty + (maxDuty - minDuty) * (new_degrees/180)) - offsetDuty
            SERVO_PIN.duty_u16(duty)
            sleep(1)
            
            SERVO_PIN.duty_u16(int(0)) # deactivate 
            sleep(1)  


    def cycle(self):

        for i in range(90, minServoAngle, -1):
            duty = int(minDuty + (maxDuty - minDuty) * (i/180)) - offsetDuty
            SERVO_PIN.duty_u16(duty)
            sleep(1)
        
        sleep(5)    
        for i in range(minServoAngle, maxServoAngle, 1):
            duty = int(minDuty + (maxDuty - minDuty) * (i/180)) - offsetDuty
            SERVO_PIN.duty_u16(duty)
            sleep(1)
        sleep(5)    
        for i in range(maxServoAngle, 89, -1):
            duty = int(minDuty + (maxDuty - minDuty) * (i/180)) - offsetDuty
            SERVO_PIN.duty_u16(duty)
            sleep(1)
        
"""Class controlling the shield servo"""

from machine import Pin, PWM
from time import sleep

SERVO_PIN = PWM(Pin(16))
SERVO_PIN.freq(50)
#SERVO_PIN.duty_ns(9000) 

servoRange = int(50)
maxServoAngle = int(90 - (50//2)) # i.e min shield angle (full moon)
minServoAngle = int(90 + (50//2)) # i.e max shield angle (full moon)

# set max and min duty
maxDuty = int(9000)
minDuty = int(1000)



class Servo():

    def __init__(self):
        
        mid_position_duty = int(minDuty+(maxDuty-minDuty)*(90/180))
        SERVO_PIN.duty_u16(mid_position_duty)
    
    
    def trackToPosition(self, current_degrees, new_degrees):
        """Track slowly to position. Called on startup and as part of reset procedure"""

        # limit angle beteen 0 and 180
        # if new_degrees > minServoAngle: new_degrees = minServoAngle
        # if new_degrees < maxServoAngle: new_degrees = maxServoAngle

        current_duty = int(minDuty+(maxDuty-minDuty)*(current_degrees/180))
        new_duty = int(minDuty+(maxDuty-minDuty)*(new_degrees/180))
        
        if current_duty < new_duty:
            for i in range(current_duty, new_duty):
                SERVO_PIN.duty_u16(i)
                sleep(0.0025)
        else:
            for i in range(current_duty, new_duty, -1):
                SERVO_PIN.duty_u16(i)
                sleep(0.0025)

        SERVO_PIN.duty_u16(int(0)) # deactivate 
        sleep(1)
 

    def trackToCentre(self):
        """Track to centre position."""
        
        duty = int(minDuty+(maxDuty-minDuty)*(90/180))

        SERVO_PIN.duty_u16(duty)
        sleep(1)
        
        SERVO_PIN.duty_u16(int(0)) # deactivate 
        sleep(1)

        

    def tickTock(self, current_degrees, new_degrees, trackToStart):
        """Tick to next shield position. Assumes step is small as fast motion."""


        if trackToStart:
            print("Tracking to start ..")
            self.trackToPosition(current_degrees, new_degrees)

        else:

            # limit angle beteen 0 and 180
            if new_degrees > 180: new_degrees=180
            if new_degrees < 0: new_degrees=0

            print("Setting angle to:", new_degrees, "degrees")
            
            # Calcuate and set servo position
            duty = int(minDuty + (maxDuty - minDuty) * (new_degrees/180))
            SERVO_PIN.duty_u16(duty)
            sleep(1)
            
            SERVO_PIN.duty_u16(int(0)) # deactivate 
            sleep(1)  
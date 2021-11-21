import ujson, utime
from machine import RTC, Pin, PWM
from time import sleep

from RTC_ds3231 import ds3231
from moon_servo import Servo, maxServoAngle, minServoAngle, servoRange

# PARAMETERS

# Servo
current_servo_degrees = int(90)
sleep_duration_ms = int(10000) # 10000 ms = 10 sec (Set to 6 hours when deploying)

# RTC object
I2C_PORT = 0
I2C_SDA = 20
I2C_SCL = 21


def setTime(_rtc_pico):
    """Used to set the initial time when first uploading to Pico board"""

    # SET rtc_ds3231 TIME
    rtc_ds3231 = ds3231(I2C_PORT,I2C_SCL,I2C_SDA)
    rtc_ds3231.set_time('20:50:00,Tuesday,2021-11-16')
    datetime = rtc_ds3231.read_time()

    # Sync to pico_rtc time    
    _rtc_pico.datetime(datetime)
    print("Datetime on DS3231 RTC:", datetime)
    print("Datetime on pico RTC:", _rtc_pico.datetime())


def convertDatetime(_datetime): 

    """Convert RTC datetime to format suitable for searching forecast dictionary (i.e "2021-12-21")"""

    year = _datetime[0]
    month = _datetime[1]
    day = _datetime[2]

    if month < 10:
        month = "0" + str(month)
    if day < 10:
        day = "0" + str(day)


    datetime = str(year) + "-" + str(month) + "-" + str(day)
    return datetime


def readLunation(_date):
    """Read json file and return current lunation"""

    with open('forecast-0-5.txt') as forecast_json:
        forecastDict = ujson.load(forecast_json)
        lunation = forecastDict[_date]
    
    print("- Date: ", _date)
    print("- Lunation today: ", lunation)

    return lunation


def calculateAngle(lunation, _current_servo_degrees):
    """
    LUNATION
    Full moon: 0.5
    New/No moon: 0, 1

    SERVO
    Full moon = 90 +/- maxShieldAngle
    New/No moon = 90 degrees

    Notes:
    - Shield tracks right in the Southern Hemisphere and left in the Northern Hemisphere.
    - If the lunation moves above 0.5, the shield should track to 1st position.

    """

    angle_pct = 0.0 # value from 0 - 1 representing shield position with respect to min and max angle.
    shield_angle_degrees = int(90)

    if(lunation < 0.5): # shield is moving right, away from centre position (new moon)
        angle_pct = lunation / 0.5
    else:
        angle_pct = (lunation - 0.5) / 0.5
    
    shield_angle_degrees = int(minServoAngle + (angle_pct * servoRange))
    servo_angle_degrees = 90 - (shield_angle_degrees - 90)

    #servoPos = minServoPos + (lunation * maxAngleOfShield)
    print("- Shield angle:", shield_angle_degrees)
    print("- Servo angle:", servo_angle_degrees)
    print("")

    trackToStart = False
    if _current_servo_degrees < servo_angle_degrees:
        trackToStart = True

    return (servo_angle_degrees, trackToStart)


def startupProcedure(_servo, _rtc):

    global current_servo_degrees

    # 1) Reset shield to start position
    print("1. Tracking to centre position ..")
    _servo.setAngle(90)

    # 2) Read lunation & update position
    print("2. Getting moon phase & updating position ..")

    today = _rtc.datetime()
    today_formatted = convertDatetime(today)
    
    lunationToday = readLunation(today_formatted)
    
    degrees_tuple = calculateAngle(lunationToday, 90) # tuple = (servo_angle_degrees, trackToStart)
    new_degrees = degrees_tuple[0]

    _servo.trackToPosition(90, new_degrees)
    current_servo_degrees = new_degrees # update global variable
    
    print("Position updated. Going to sleep for:", sleep_duration_ms/1000, "seconds")
    machine.lightsleep(sleep_duration_ms)
    print("")

    return new_degrees


def wakeSleepCycle(_servo, _rtc):

    global current_servo_degrees
    
    print("Waking & updating position")
    today = _rtc.datetime()
    today_formatted = convertDatetime(today)
    lunationToday = readLunation(today_formatted)
    
    degrees_tuple = calculateAngle(lunationToday, current_servo_degrees)
    new_degrees = degrees_tuple[0]
    trackToStart = degrees_tuple[1]
    
    # Set angle
    _servo.tickTock(current_servo_degrees, new_degrees, trackToStart)

    # update global variable to current angle
    current_servo_degrees = new_degrees
    print("Position updated. Going to sleep for:", sleep_duration_ms/1000, "seconds")
    machine.lightsleep(sleep_duration_ms)
    print("")



# INIT RTC
rtc_pico = RTC() 
setTime(rtc_pico) # Uncomment this line when uploading main.py
rtc_pico.datetime((2021, 11, 19, 1, 23, 59, 45, 0)) # hard-coded datetime used for testing
servo = Servo()

# A) STARTUP (Tracking Mode)
# startupProcedure(servo, rtc_pico)
# while True:       
#     wakeSleepCycle(servo, rtc_pico)


# B) Demo mode
servo.setAngle(int(90))
sleep(1)
while True:           
    servo.cycle()
    print("repeat")

# C) Calibration mode
#servo.setAngle(int(70))

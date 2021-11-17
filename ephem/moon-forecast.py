#!/usr/bin/python
import datetime
import ephem
import ujson
import json


years = int(5)
today = datetime.date.today()

# Lunation:
# full moon: 0.5
# New: 0, 1

# Servo:
# full moon = maxAngleOfShield (left + right)
# New moon = servo: 90 degrees


def get_phase_on_day(year,month,day):
  """Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
  #Ephem stores its date numbers as floating points, which the following uses
  #to conveniently extract the percent time between one new moon and the next
  #This corresponds (somewhat roughly) to the phase of the moon.

  #Use Year, Month, Day as arguments
  date=ephem.Date(datetime.date(year,month,day))
  nnm = ephem.next_new_moon    (date)
  pnm = ephem.previous_new_moon(date)
  lunation=(date-pnm)/(nnm-pnm)

  lunation = round(lunation, 2)

  return lunation



# Calculate lunation for each day for the next X years, store in JSON file
def forecastLunarPhase(dateToday):

    forecastDict = {}
    currentDate = dateToday
    for i in range(int(365.25*years)):
        lunationToday = get_phase_on_day(currentDate.year, currentDate.month, currentDate.day)
        #forecastList.append((currentDate, lunationToday))
        forecastDict[str(currentDate)] = lunationToday
        currentDate += datetime.timedelta(days=1)

    # # convert dict to json
    # forecastJSON = ujson.dumps(forecastDict)
    # return forecastJSON

    with open('forecast-0-5.txt', 'w') as outfile:
        json.dump(forecastDict, outfile)



phase = get_phase_on_day(2027, 5, 6)
#phase = get_phase_on_day(today.year, today.month, today.day)

print("Lunation: ", phase)
#print("Current date: ", today)
print()
# output json file:
forecastLunarPhase(today)

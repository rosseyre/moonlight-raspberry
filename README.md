# moonlight-raspberry

Source code for lighting design project, 'the long now'.

Project Info: http://arkology.co.za/moonlight

- Moon-phase tracking using data generated from the Ephem astronomical python library
- Servo control and external RTC module integration with the Raspberry Pi Pico

## Project structure:

1. ephem | contains a .py file used to calculate lunation values and output a forecast (JSON)
2. MicroPython | installation file for bootloading MicroPython on the Raspberry Pi Pico (hold Bootsel button on Pico and connect USB to load)
3. pico | folder containing modules used to control the Pico once deployed. 'main.py' runs automatically once the board receives power.

## Raspberry Pi Pico setup:

- Install MicroPython
- Install Pico-Go VS code extension to interface with the board via the terminal or, alternatively, use the Thonny IDE.

## Dependencies:

1. Epem

pip install ephem

PyEphem provides an ephem Python package for performing high-precision astronomy computations
https://pypi.org/project/ephem/

Used to generate JSON file containing daily lunation values for our moon.

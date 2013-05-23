#!/usr/bin/python
#Tells us the light is not connected

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from time import time, sleep
from subprocess import Popen, PIPE

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Turn on LCD
lcd.clear()
lcd.backlight(lcd.ON)

# Display Warning
last = int(time())
message_num = 2
waiting = True
while waiting:
    if int(time()) >= last + 2:
        lcd.clear()
        last = int(time())
        if message_num == 2:
            lcd.message("USB Light cable\nis disconnected!")
            message_num = 1
        elif message_num == 1:
            lcd.message("Plug in and\npress \"Select\".")
            message_num = 2
    if lcd.buttonPressed(lcd.SELECT):
        waiting = False

# Button has been pressed, try again.
lcd.clear()
sleep(2)
process = Popen('/etc/rc.local',stdout=PIPE)

#!/usr/bin/python
# Controls the cap!

import MySQLdb as mdb
from config import *
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Clear display and show greeting, pause 1 sec
lcd.clear()
lcd.backlight(lcd.ON)
lcd.message("Control-my-Cap\nWrist Interface")
sleep(1)

#conn = mdb.connect(host, user, passwd, db)
#
#while
#with conn:
#    try:
#        cur = conn.cursor()
#        sqlstring = "SELECT * FROM colors"
#        cur.execute(sqlstring)
#        result={'success':'true','message':'Thanks ' + twitter + '! Your color has been added to the queue.'} 
#    except:
#        result={'success':'false','message':'Something went wrong!  Your color could not be added to the queue.'}
#conn.close()

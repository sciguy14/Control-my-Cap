#!/usr/bin/python
# Controls the cap!

####
# IMPORT LIBRARIES AND CONFIGS
####
import MySQLdb as mdb
from config import *
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import check_output
import socket

####
# FUNCTIONS
####


# FUNCTION TO FACILIATE MENU SCROLLING
def update_menu(index_selected, num_items, menu_items):
    lcd.clear()
    if index_selected % 2 == 0 and num_items>(index_selected+1):
        lcd.message('>' + menu_items[index_selected][1:] + '\n' + menu_items[index_selected+1])
    elif index_selected % 2 == 0 and num_items<=(index_selected+1):
        lcd.message('>' + menu_items[index_selected][1:])
    else:
        lcd.message(menu_items[index_selected-1] + '\n>' + menu_items[index_selected][1:])

####
# MAIN PROGRAM
####

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Clear display and show greeting, pause 2 secs
lcd.clear()
lcd.backlight(lcd.ON)
backlight_state = 1
lcd.message("Control-my-Cap\nWrist Interface")
sleep(2)

# THE FOLLOWING SCREEN STATES EXIST
# top:          This is the top-level Menu.
# mode:         This is menu for selecting the cap operation mode from a list
# modeConfirm:  This is the confirmation screen for the mode selection
# brightness:   This is the brightness setting screen
# status:       This is the status monitoring screen

# We started at the top-level menu
state = 'top'

looping = True
top_menu_pointer = 0
while looping:
    lcd.clear()
    sleep(.3)
    if  state == 'top':
        top_menu =  [
                        ' Cap Mode',
                        ' Cap Brightness',
                        ' Toggle Bklight',
                        ' Status'
                    ]
        top_menu_length = len(top_menu)
        
        update_menu(top_menu_pointer, top_menu_length, top_menu) 
        waiting = True
        while waiting:
            if lcd.buttonPressed(lcd.UP) and top_menu_pointer != 0:
                top_menu_pointer = top_menu_pointer - 1
                update_menu(top_menu_pointer, top_menu_length, top_menu)
                sleep(.3)
            elif lcd.buttonPressed(lcd.DOWN) and top_menu_pointer < top_menu_length-1:
                top_menu_pointer = top_menu_pointer + 1
                update_menu(top_menu_pointer, top_menu_length, top_menu)
                sleep(.3)
            elif lcd.buttonPressed(lcd.SELECT) or lcd.buttonPressed(lcd.RIGHT):
                if top_menu_pointer == 0:
                    state = 'mode'
                    waiting = False
                elif top_menu_pointer == 1:
                    state = 'brightness'
                    waiting = False
                elif top_menu_pointer == 2:
                    if backlight_state == 1:
                        lcd.backlight(lcd.OFF)
                        backlight_state = 0
                    else:
                        lcd.backlight(lcd.ON)
                        backlight_state = 1
                    waiting = True
                    sleep(.3)
                elif top_menu_pointer == 3:
                    state = 'status'
                    waiting = False
    
    elif state == 'mode':
        mode_menu_pointer = 0
        mode_menu = [
                        ' Pretty Colors',
                        ' Web-Controlled'
                    ]
        mode_menu_length = len(mode_menu)
    elif state == 'modeConfirm':
        test=True
    elif state == 'brightness':
        test=True
    elif state == 'status':
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("1.2.3.4",9))	
            client = s.getsockname()[0]
            lcd.message("Local IP:\n" + client)
        except socket.error:
            lcd.message("Local IP:\nNULL")
        finally:
            del s
        waiting = True
        while waiting:
            if lcd.buttonPressed(lcd.LEFT):
                state = 'top'
                waiting = False
                sleep(.3)

    else:
        # Something has gone very wrong.  Kill the loop.
        looping = False

       

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



#!/usr/bin/python
# Menu and Control Interface

####
# IMPORT LIBRARIES AND CONFIGS
####
import MySQLdb as mdb
from config import *
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from subprocess import check_output
import socket, os

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
# TABLES
####

top_menu =  [
                ' Cap Mode',
                ' Cap Brightness',
                ' Toggle Bklight',
                ' Status'
            ]

mode_menu = [
                ' Web-Controlled',
                ' Rainbow',
                ' Red',
                ' Green',
                ' Blue',
                ' White',
                ' Teal',
                ' Purple',
                ' Orange',
                ' Off'
            ]



brightness_screens =  [
                        'Cap Brightness:\n#            10%',
                        'Cap Brightness:\n##           20%',
                        'Cap Brightness:\n###          30%',
                        'Cap Brightness:\n####         40%',
                        'Cap Brightness:\n#####        50%',
                        'Cap Brightness:\n######       60%',
                        'Cap Brightness:\n#######      70%',
                        'Cap Brightness:\n########     80%',
                        'Cap Brightness:\n#########    90%',
                        'Cap Brightness:\n##########  100%',
                      ]


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
        # get current mode setting from the local database
        local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
        with local_conn:
            cur = local_conn.cursor()
            sqlstring = "SELECT `value` FROM config WHERE `option` = 'mode'"
            cur.execute(sqlstring)
            sql_mode = int(cur.fetchone()[0])
        local_conn.close()
        mode_menu_pointer = sql_mode 
        mode_menu_length = len(mode_menu)
        update_menu(mode_menu_pointer, mode_menu_length, mode_menu) 
        waiting = True
        while waiting:
            if lcd.buttonPressed(lcd.UP) and mode_menu_pointer != 0:
                mode_menu_pointer = mode_menu_pointer - 1
                update_menu(mode_menu_pointer, mode_menu_length, mode_menu)
                sleep(.3)
            elif lcd.buttonPressed(lcd.DOWN) and mode_menu_pointer < mode_menu_length-1:
                mode_menu_pointer = mode_menu_pointer + 1
                update_menu(mode_menu_pointer, mode_menu_length, mode_menu)
                sleep(.3)
            elif lcd.buttonPressed(lcd.LEFT):
                state = 'top'
                waiting = False
                sleep(.3)
            elif lcd.buttonPressed(lcd.SELECT) or lcd.buttonPressed(lcd.RIGHT):
                state = 'modeConfirm'
                MODE = mode_menu_pointer
                waiting = False
    elif state == 'modeConfirm':
        lcd.message ('Setting Mode to:\n' + mode_menu[MODE][1:])
        local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
        with local_conn:
            cur = local_conn.cursor()
            sqlstring = "UPDATE config SET `value`=" + str(MODE) + " WHERE `option`='mode'"
            cur.execute(sqlstring)
        local_conn.close()
        lcd.clear()
        lcd.message ('Mode set to:\n' + mode_menu[MODE][1:])
        sleep(2)
        lcd.clear()
        lcd.message ('Press Select\nto go home.')
        waiting = True
        while waiting:
            if lcd.buttonPressed(lcd.SELECT):
                state = 'top'
                waiting = False
                sleep(.3)
    elif state == 'brightness':
        # get current brightness setting from the local database
        local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
        with local_conn:
            cur = local_conn.cursor()
            sqlstring = "SELECT `value` FROM config WHERE `option` = 'brightness'"
            cur.execute(sqlstring)
            brightness = int(cur.fetchone()[0])
        local_conn.close()
        lcd.clear
        lcd.message(brightness_screens[(brightness/10)-1])
        waiting = True
        while waiting:
            if lcd.buttonPressed(lcd.DOWN) and brightness > 10:
                brightness = brightness - 10
                local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
                with local_conn:
                    cur = local_conn.cursor()
                    sqlstring = "UPDATE config SET `value`=" + str(brightness) + " WHERE `option`='brightness'"
                    cur.execute(sqlstring)
                local_conn.close()
                lcd.clear()
                lcd.message(brightness_screens[(brightness/10)-1])
                sleep(.3)
            elif lcd.buttonPressed(lcd.UP) and brightness < 100:
                brightness = brightness + 10
                local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
                with local_conn:
                    cur = local_conn.cursor()
                    sqlstring = "UPDATE config SET `value`=" + str(brightness) + " WHERE `option`='brightness'"
                    cur.execute(sqlstring)
                local_conn.close()
                lcd.clear()
                lcd.message(brightness_screens[(brightness/10)-1])
                sleep(.3)
            elif lcd.buttonPressed(lcd.LEFT):
                state = 'top'
                waiting = False
                sleep(.3)
    elif state == 'status':
        # get current mode setting from the local database
        local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
        with local_conn:
            cur = local_conn.cursor()
            sqlstring = "SELECT `value` FROM config WHERE `option` = 'mode'"
            cur.execute(sqlstring)
            sql_mode = int(cur.fetchone()[0])
        local_conn.close()

        #Get current IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("1.2.3.4",9))	
            client = s.getsockname()[0]
        except socket.error:
            client = "WiFi Down"
        finally:
            del s

        lcd.message(mode_menu[sql_mode][1:] + '\n' + client)
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



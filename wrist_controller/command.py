#!/usr/bin/python
# Serial Command Script

####
# IMPORT LIBRARIES AND CONFIGS
####
import MySQLdb as mdb
import serial, math
from config import *
from time import time


####
# MAIN PROGRAM
####
fade_time = 1000 #ms
buffer_time = 2  #seconds
last_mode = -1
last_scale = 0
rainbow_state = 0
last = int(time())

rainbow_cycle = [
                    (0.0,0.0,0.0,0.0),
                    (255.0,0.0,0.0,0.0),
                    (255.0,255.0,0.0,0.0),
                    (255.0,255.0,255.0,0.0),
                    (0.0,255.0,255.0,255.0),
                    (0.0,255.0,255.0,0.0),
                    (0.0,0.0,255.0,0.0),
                    (255.0,0.0,255.0,0.0),
                    (255.0,0.0,255.0,255.0),
                    (0.0,0.0,255.0,255.0),
                    (0.0,0.0,0.0,255.0),
                    (0.0,255.0,0.0,255.0),
                    (255.0,255.0,0.0,255.0),
                    (0.0,255.0,0.0,0.0)
                ]
rainbow_max_index = len(rainbow_cycle)-1                    

while True:
    # Look at the local database to determine the operation mode and brightness.
    local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
    with local_conn:
        cur = local_conn.cursor()
        sqlstring = "SELECT `value` FROM config WHERE `option` = 'mode'"
        cur.execute(sqlstring)
        mode = int(cur.fetchone()[0])
        sqlstring = "SELECT `value` FROM config WHERE `option` = 'brightness'"
        cur.execute(sqlstring)
        scale = (float(cur.fetchone()[0]))/100.0
    local_conn.close()

    #If something has changed, issue an update to the cap!
    #If it's time for a rainbow update, do that.
    if mode != last_mode or scale != last_scale or (int(time()) >= last + buffer_time and mode == 1):

        # Setup the Serial Port
        ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

        #Web-Controlled
        if mode == 0:
            #do stuff
            thing=True

        #Rainbow
        elif mode == 1:
            if rainbow_state > rainbow_max_index:
                rainbow_state = 0
            last = int(time())    
            ser.write(".a:3:" + str(int(math.floor(rainbow_cycle[rainbow_state][0]*scale))) + "," + str(int(math.floor(rainbow_cycle[rainbow_state][1]*scale))) + "," + str(int(math.floor(rainbow_cycle[rainbow_state][2]*scale))) + "," + str(int(math.floor(rainbow_cycle[rainbow_state][3]*scale))) + "," + str(fade_time) + "\n")
            rainbow_state = rainbow_state + 1

        #Red
        elif mode == 2:
            ser.write(".a:3:" + str(int(math.floor(255.0*scale))) + ",0,0,0," + str(fade_time) + "\n")
            
        #Green
        elif mode == 3:
            ser.write(".a:3:0," + str(int(math.floor(255.0*scale))) + ",0,0," + str(fade_time) + "\n")
        #Blue
        elif mode == 4:
            ser.write(".a:3:0,0," + str(int(math.floor(255.0*scale))) + ",0," + str(fade_time) + "\n")
        #White
        elif mode == 5:
            ser.write(".a:3:0,0,0," + str(int(math.floor(255.0*scale))) + "," + str(fade_time) + "\n")
        #Teal
        elif mode == 6:
            ser.write(".a:3:0," + str(int(math.floor(255.0*scale))) + "," + str(int(math.floor(255.0*scale))) + ",0," + str(fade_time) + "\n")
        #Purple
        elif mode == 7:
            ser.write(".a:3:" + str(int(math.floor(255.0*scale))) + ",0," + str(int(math.floor(255.0*scale))) + ",0," + str(fade_time) + "\n")
        #Orange
        elif mode == 8:
            ser.write(".a:3:" + str(int(math.floor(255.0*scale))) + "," + str(int(math.floor(255.0*scale))) + ",0,0," + str(fade_time) + "\n")
        #Off
        elif mode == 9:
            ser.write(".a:3:0,0,0,0," + str(fade_time) + "\n")

        #Close the Serial port
        ser.close()

        #Update tracking variables
        last_mode = mode
        last_scale = scale


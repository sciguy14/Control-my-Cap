#!/usr/bin/python
# Serial Command Script

####
# IMPORT LIBRARIES AND CONFIGS
####
import MySQLdb as mdb
import serial, math, urllib2, json, os
from config import *
from time import time
from twitter import *

####
# FUNCTIONS
####

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))


####
# MAIN PROGRAM
####
fade_time = 1000 #ms
buffer_time = 2  #seconds
last_mode = -1
last_scale = 0
rainbow_state = 0
web_state = 0
last_tweeted = 1
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

web_cycle = [
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0),
                    (0.0,0.0,0.0)
            ]
web_max_index = len(web_cycle)-1

twitter_set = False

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
        sqlstring = "SELECT `value` FROM config WHERE `option` = 'last_tweeted'"
        cur.execute(sqlstring)
        last_tweeted = int(cur.fetchone()[0])
    local_conn.close()

    #If we're in web mode for the first time, authenticate w/ Twitter Oauth
    if mode == 0 and twitter_set == False:
        MY_TWITTER_CREDS = os.path.expanduser('/home/pi/.my_app_credentials')
        if not os.path.exists(MY_TWITTER_CREDS):
            oauth_dance("Jeremy's Cap", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)
        oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
        twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
        twitter_set = True


    # If we're in web mode, update the web cycle matrix
    if mode == 0:
        data = urllib2.urlopen('http://controlmycap.com/cgi-bin/retrieve.py').read()
        data = json.loads(data);
        for i in range(len(web_cycle)):
            data[i][2] = str(data[i][2])
            data[i][3] = str(data[i][3])
            data[i][4] = str(data[i][4])
            rgb = hex_to_rgb(data[i][4])
            web_cycle[i] = list(web_cycle[i])
            web_cycle[i][0] = float(rgb[0])
            web_cycle[i][1] = float(rgb[1])
            web_cycle[i][2] = float(rgb[2])
            #tweet it if this is being added for the first time!
            if data[i][0] > last_tweeted:
                #tweet it
                if data[i][3] == "":
                    name = data[i][2]
                else:
                    name = data[i][3]
                hex_color = data[i][4]
                tweet = "Thanks " + name + "! I'm about to cycle to your color: " + hex_color + " (ID: " + str(data[i][0]) + ")"
                twitter.statuses.update(status=tweet)
                #update local database
                local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
                with local_conn:
                    cur = local_conn.cursor()
                    sqlstring = "UPDATE config SET `value`=" + str(data[i][0]) + " WHERE `option`='last_tweeted'"
                    cur.execute(sqlstring)
                local_conn.close()
    

    #If something has changed, issue an update to the cap!
    #If it's time for a rainbow update, do that.
    #If it's time for a web cycle update, do that.
    if mode != last_mode or scale != last_scale or (int(time()) >= last + buffer_time and (mode == 1 or mode == 0)):

        # Setup the Serial Port
        ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

        #Web-Controlled
        if mode == 0:
            if web_state > web_max_index:
                web_state = 0
            last = int(time())
            ser.write(".a:3:" + str(int(math.floor(web_cycle[web_state][0]*scale))) + "," + str(int(math.floor(web_cycle[web_state][1]*scale))) + "," + str(int(math.floor(web_cycle[web_state][2]*scale))) + ",0," + str(fade_time) + "\n")
            web_state = web_state + 1

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


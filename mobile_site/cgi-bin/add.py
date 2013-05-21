#!/usr/bin/python
# Adds to the database.

import sys,json,re
import MySQLdb as mdb
from config import *

myjson = json.load(sys.stdin)
conn = mdb.connect(host, user, passwd, db)

twitter = conn.escape_string(str(myjson["twitter"]))
color = conn.escape_string(str(myjson["color"]))

#Check for unfilled form entries.
if not twitter:
        result={'success':'false','message':'You must enter a valid twitter handle!'}
elif not color:
        result={'success':'false','message':'You must pick a color!'}
else:

        #Make sure twitter username starts with an "@".
        if not twitter.startswith('@'):
                twitter = '@' + twitter
                

        #Do a Regex Check on the twitter username to ensure validity (I think this is right...)
        valid = re.search( r'^@(\w+)', twitter)


        if valid:
                with conn:
                        try:
                                cur = conn.cursor()
                                sqlstring = "INSERT INTO colors (twitter, color) VALUES ('" + twitter + "', '" + color + "')"
                                cur.execute(sqlstring)
                                result={'success':'true','message':'Thanks ' + twitter + '! Your color has been added to the queue.'} 
                        except:
                                result={'success':'false','message':'Something went wrong!  Your color could not be added to the queue.'}
        else:
                result={'success':'false','message':'Your Twitter Handle is invalid!'}

conn.close()
print 'Content-Type: application/json\n\n'
print json.JSONEncoder().encode(result)

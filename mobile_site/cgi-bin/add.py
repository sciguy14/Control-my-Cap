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
	result={'success':'false','message':'You must enter a valid twitter handle or name!<br />Alphanumerics & Underscores only.'}
elif not color:
	result={'success':'false','message':'You must pick a color!'}
else:
	valid = False
	#Make sure twitter username starts with an "@".
	if twitter.startswith('@'):
		name = twitter[1:]
		valid = re.search( r'^@(\w+)', twitter)
	else:
		name = twitter
		twitter = ""
		valid = re.search( r'^\w+$', name)
			
	#Do a Regex Check on the twitter_handle/name to ensure validity

	if valid:
		with conn:
			try:
				cur = conn.cursor()
				sqlstring = "INSERT INTO colors (name, twitter, color) VALUES ('" + name + "', '" + twitter + "', '" + color + "')"
				cur.execute(sqlstring)
				result={'success':'true','message':'Thanks ' + name + '! Your color has been added to the queue.'} 
			except:
				result={'success':'false','message':'Something went wrong!<br />Your color could not be added to the queue.'}
	else:
		result={'success':'false','message':'Your Twitter Handle or Name is Invalid!<br />Alphanumerics & Underscores only.'}

conn.close()
print 'Content-Type: application/json\n\n'
print json.JSONEncoder().encode(result)

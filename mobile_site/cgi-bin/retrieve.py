#!/usr/bin/python

import sys,json,datetime,calendar
import MySQLdb as mdb
from config import *

conn = mdb.connect(host, user, passwd, db)
with conn:
    cur = conn.cursor()
    sqlstring = "SELECT * FROM colors ORDER BY `index` DESC LIMIT 10"
    cur.execute(sqlstring)
    colors = list(cur.fetchall())
conn.close()
for i in range(10):
    colors[i] = list(colors[i])
    colors[i][1] = calendar.timegm(colors[i][1].timetuple())

colors.reverse()  
print 'Content-Type: application/json\n'
print json.JSONEncoder().encode(colors)

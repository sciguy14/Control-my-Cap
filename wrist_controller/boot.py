#!/usr/bin/python
# Boot script. Boot state is lights off.

import MySQLdb as mdb
from config import *

local_conn = mdb.connect(local_host, local_user, local_passwd, local_db)
with local_conn:
    cur = local_conn.cursor()
    sqlstring = "UPDATE config SET `value`=9 WHERE `option`='mode'"
    cur.execute(sqlstring)
local_conn.close()

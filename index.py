"""
CGI link shortener module
Copyright (c) 2014 Tyler Philbrick
See COPYING for license details
"""

import cgi
import sqlite3

#import cgitb  #Uncomment for verbose error messages
#cgitb.enable()

SERVERN = "quetzal.vms.pw" #replace with automatic hostname id'ing

conn = sqlite3.connect("/run/lighttpd/urls.db")
c = conn.cursor()
c.execute("""
	CREATE TABLE IF NOT EXISTS urls
	(id INTEGER PRIMARY KEY, url TEXT);
""")
conn.commit()

args = cgi.FieldStorage()
if "url" in args:
	url = args["url"].value
	c.execute("INSERT INTO urls VALUES (NULL, ?);", (url,))
	conn.commit()
	id = c.lastrowid
	print("http://{servern}/?id={id}".format(servern=SERVERN, id=id))

elif "id" in args:
	id = args["id"].value
	c.execute("SELECT * FROM urls WHERE id=?;", (id,))
	url = c.fetchone()
	if url is None:
		print("ID Not valid")
	else:
		print(url[1])

conn.close()

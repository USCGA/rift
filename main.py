#!/usr/bin/env python3
import redis, sys
from flask import Flask, render_template, Markup
from lib import nav

# APP CONFIGURATION
app = Flask(__name__)
app.jinja_env.line_statement_prefix = '%'

# PARAMETERS
redis_host = '127.0.0.1'
redis_port = 6379

print("[+] Starting portal.")

# REDIS Connection
db = redis.Redis(host=redis_host, port=redis_port)
print("[i] Connecting to redis server at " + redis_host + ":" + str(redis_port) + ".")
try:
	print("[+] Connected: Redis v" + db.info(section='server')['redis_version']);
except:
	print("[-] Could not establish connection to redis. Check config.")
	print("[-] Stopping.")
	sys.exit()

@app.route("/")
def root():
	menu = nav.items
	return render_template('home.html', menu=menu, db_version=db.info(section='server')['redis_version'])

@app.route("/login")
def login():
	menu = nav.items
	return render_template('login.html', menu=menu, db_version=db.info(section='server')['redis_version'])

# EXECUTABLE 
# (Unnecessary if this file is not the entrypoint)
# Keep this here if you're using the Flask development server.
if __name__ == '__main__':
    app.run()

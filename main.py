#!/usr/bin/env python3
from flask import Flask, render_template, Markup
import redis, sys
app = Flask(__name__)

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
    title = "USCGA CYBER"
    header = "OK"
    content = Markup('<p>Everything seems to be working properly.</p><p>Redis %s</p>') % db.info(section='server')['redis_version']
    return render_template('base.html', title=title, header=header, content=content)

# EXECUTABLE 
# (Unnecessary if this file is not the entrypoint)
if __name__ == '__main__':
    app.run()

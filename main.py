#!/usr/bin/env python3
from flask import Flask
import redis
app = Flask(__name__)

redis_host = '127.0.0.1'
redis_port = 6379

print("[+] Starting portal.")

# REDIS Connection
db = redis.Redis(host=redis_host, port=redis_port)
print("[i] Connecting to redis server at " + redis_host + ":" + str(redis_port))
try:
	print("[+] Connected: Redis v" + db.info(section='server')['redis_version']);
except:
	print("[-] Could not establish connection to redis.")


@app.route("/")
def hello():
    return "Awww... Puppy!"

if __name__ == '__main__':
    app.run()

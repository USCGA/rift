#!/usr/bin/env python3
from flask import Flask
app = Flask(__name__)

print("[!] Starting server.")

@app.route("/")
def hello():
    return "Awww... Puppy!"

if __name__ == '__main__':
    app.run()

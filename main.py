#!/usr/bin/env python3
import sys
from flask import Flask, render_template, Markup
from lib import nav
from flask_mongoengine import MongoEngine
from flask_security import Security, MongoEngineUserDatastore, \
	UserMixin, RoleMixin, login_required

# App Configuration
app = Flask(__name__)
app.jinja_env.line_statement_prefix = '%'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'salt'

# MongoDB Config
app.config['MONGODB_DB'] = 'rift'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017


# Create database connection object
db = MongoEngine(app)

print("[+] Starting portal.")


@app.route("/")
def root():
	menu = nav.items
	return render_template('home.html', menu=menu, db_version="Disconnected")

@app.route("/login")
def login():
	menu = nav.items
	return render_template('login.html', menu=menu, db_version="Disconnected")

# EXECUTABLE 
# (Unnecessary if this file is not the entrypoint)
# Keep this here if you're using the Flask development server.
if __name__ == '__main__':
    app.run()

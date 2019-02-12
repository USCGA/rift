from flask import Blueprint, render_template, request, escape, session, redirect, url_for
from mongoengine import Document, DoesNotExist, MultipleObjectsReturned
from passlib.hash import pbkdf2_sha256
import rift.nav as nav
import rift.models as models

# All routes defined below belong to the "main" blueprint 
# which is applied to flask.app in __init__.py.
main = Blueprint("pages", __name__)

### ROUTES ###

@main.route("/")
def index():
	login_status = login_status_string(session)
	menu = nav.items
	return render_template('home.html', menu=menu, Motd=models.Motd, login_status=login_status)

@main.route("/login", methods=['GET','POST'])
def page_login():
	login_status = login_status_string(session)
	# TODO Add validation to email/uname/pword.
	if request.method == 'POST':
		if request.form['type'] == "login": # ----------- LOGIN
			uname = request.form['uname']
			pword = request.form['pword']
			login_user(uname, pword)
		elif request.form['type'] == "register": # ------ REGISTER
			uname = request.form['uname']
			email = request.form['email']
			pword = request.form['pword']
			register_user(uname, email, pword)
		return redirect(url_for("pages.index"))
	if request.method == 'GET':
		menu = nav.items
		return render_template('login.html', menu=menu, login_status=login_status)


### FUNCTIONS ###

def login_status_string(session):
	# Check if valid session.
	if 'username' in session:
		status = 'Logged in as %s' % escape(session['username'])
	else:
		status = 'You are not logged in.'
	return status

def login_user(username, password):
	'''
	Login username by retrieving hashed pword stored in database
	and comparing to password. Return False if failure.
	'''
	# Retrieve user from db.
	try:
		user = models.User.objects.get(username=username)
	except DoesNotExist:
		return False
	except MultipleObjectsReturned:
		return False
	# Ensure password match.
	if pbkdf2_sha256.verify(password, user.password):
		# Good Login.
		# Create session
		session['username'] = username
		return True
	else:
		# Bad Login.
		return False

def register_user(username, email, password):
	'''
	Register a new user with username, email, and password.
	Return False if failure.
	'''
	# Hash password.
	pword_hash = pbkdf2_sha256.hash(password)
	# Create New User.
	new_user = models.User()
	new_user.email = email
	new_user.username = username
	new_user.password = pword_hash
	new_user.save()
	# TODO Login after successful login
	return True
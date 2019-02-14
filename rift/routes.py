from flask import Blueprint, render_template, request, escape, session, redirect, url_for
from mongoengine import Document, DoesNotExist, MultipleObjectsReturned
from passlib.hash import pbkdf2_sha256
import rift.nav as nav
import rift.models as models

# All routes defined below belong to the "main" blueprint 
# which is applied to flask.app in __init__.py.
main = Blueprint("pages", __name__)


# Simple Config
# Variables we might want to change later.
default_screenname = "guest"

### ROUTES ###

@main.route("/")
def index():
	# Change screenname and session_button based on login status.
	if logged_in(session):
		logged_user = user_info(session)
	screenname = (logged_user.username.lower() if logged_in(session) else default_screenname)
	session_button = (nav.Logout if logged_in(session) else nav.Login)

	menu = nav.default_menu # The default menu is always displayed right now.
	return render_template('home_v2.html', menu=menu, screenname=screenname, session_button=session_button)

@main.route("/login", methods=['GET','POST'])
def page_login():
	if logged_in(session):
		logged_user = user_info(session)
	screenname = (logged_user.username.lower() if logged_in(session) else default_screenname)
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
		menu = nav.default_menu
		return render_template('login.html', menu=menu, user=screenname)

@main.route("/logout")
def page_logout():
	session.clear()
	return redirect(url_for('pages.index'))


### FUNCTIONS ###

def logged_in(session):
	if 'username' in session:
		return True
	else:
		return False

def user_info(session):
	# Check if valid session.
	if 'username' in session:
		user = models.User.objects.get(username=session['username'])
		return user
	else:
		return False

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
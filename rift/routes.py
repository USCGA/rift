from flask import Blueprint, render_template, request, \
	escape, session, redirect, url_for, flash, Response
from mongoengine import Document, DoesNotExist, MultipleObjectsReturned, NotUniqueError, ValidationError
from passlib.hash import pbkdf2_sha256
from enum import Enum
import rift.nav as nav
import rift.models as models

# All routes defined below belong to the "main" blueprint 
# which is applied to flask.app in __init__.py.
main = Blueprint("pages", __name__)


# --- Simple Config ---
# Variables we might want to change later.
default_screenname = "guest"
# TODO relocate to separate config.
min_pwd_length = 8
max_pwd_length = 24
min_usr_length = 4
max_usr_length = 16

### CLASSES ###
class LoginStatus(Enum):
	success = 1
	bad_username = 2
	bad_password = 3
	multiple_usr = 4

class RegisterStatus(Enum):
	success = 1
	bad_username = 2
	bad_password = 3
	bad_validation = 4
	not_unique = 5

### ROUTES ###

@main.route("/")
def index():
	# Change screenname and session_button based on login status.
	if logged_in(session):
		logged_user = user_info(session)
	screenname = (logged_user.username.lower() if logged_in(session) else default_screenname)
	session_button = (nav.Logout if logged_in(session) else nav.Login)

	menu = nav.default_menu # The default menu is always displayed right now.
	return render_template(
		'home_v2.html', 
		menu=menu, 
		screenname=screenname)

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
			result = login_user(uname, pword)
			
		elif request.form['type'] == "register": # ------ REGISTER
			uname = request.form['uname']
			email = request.form['email']
			pword = request.form['pword']
			result = register_user(uname, email, pword)

		return Response(status=200)
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
		flash("No passwd entry for user '"+ username +"'")
		return LoginStatus.bad_username
	except MultipleObjectsReturned:
		flash("Somehow, there are multiple users by that name. Contact admin.")
		return LoginStatus.multiple_usr
	# Ensure password match.
	if pbkdf2_sha256.verify(password, user.password):
		# Good Login.
		# Create session
		session['username'] = username
		return LoginStatus.success
	else:
		# Bad Login.
		flash("su: Authentication failure")
		return LoginStatus.bad_password

def register_user(username, email, password):
	'''
	Register a new user with username, email, and password.
	Return False if failure.
	'''
	# Validation #TODO Improve validation, move to separate function.
	if (username == "undefined"):
		flash("Username '" + username +"' not permitted.")
		flash("`adduser [username]`")
		return RegisterStatus.bad_validation

	# Username length
	if (len(username) < min_usr_length):
		flash("Username must be longer than " + str(min_usr_length) + " characters.")
		return RegisterStatus.bad_validation
	if (len(username) > max_usr_length):
		flash("Username must be shorter than " + str(max_usr_length) + " characters.")
		return RegisterStatus.bad_validation

	# Password length
	if (len(password) < min_pwd_length):
		flash("Password must be longer than " + str(min_pwd_length) + " characters.")
		return RegisterStatus.bad_validation
	if (len(password) > max_pwd_length):
		flash("Password must be shorter than " + str(max_pwd_length) + " characters.")
		return RegisterStatus.bad_validation

	# Hash password.
	pword_hash = pbkdf2_sha256.hash(password)
	# Create New User.
	new_user = models.User()
	new_user.email = email
	new_user.username = username
	new_user.password = pword_hash
	try:
		new_user.save()
	except NotUniqueError as e:
		flash(str(e))
		return RegisterStatus.not_unique
	except ValidationError as e:
		flash(str(e))
		return RegisterStatus.bad_validation
	# TODO Login after successful login
	return RegisterStatus.success
from flask import flash, session
from passlib.hash import pbkdf2_sha256
from mongoengine import Document, DoesNotExist, MultipleObjectsReturned, NotUniqueError, ValidationError
from enum import Enum
import rift.models as models
import warnings

# --- Configuration --- #
# TODO Relocate to a central configuration file
min_pwd_length = 8
max_pwd_length = 24
min_usr_length = 4
max_usr_length = 16


### ENUMERABLES ###

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


### FUNCTIONS ###

def LoggedIn(session):
	if 'username' in session:
		return True
	else:
		return False

def GetUserObject(session):
	# Check if valid session.
	if 'username' in session:
		user = models.User.objects.get(username=session['username'])
		return user
	else:
		return False

def ScoreChallenge(user, challengeDocument):
	userDocument = models.User.objects.only('completed_challenges', 'score').get(id=user.id)
	if (challengeDocument in userDocument.completed_challenges):
		warnings.warn(user.username + " attempted to score a challenge \"" + challengeDocument.title + "\" twice.", UserWarning, stacklevel=2)
	else:
		userDocument.modify(inc__score=challengeDocument.point_value, push__completed_challenges=challengeDocument)

def Login(username, password):
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

def Register(firstName, lastName, username, email, password, rpass):
	'''
	Register a new user with first name, last name, username, email, and password.
	Return False if failure.
	'''
	# Validation #TODO Improve validation.
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

	# Password and Repeat Password Identical
	if (password != rpass):
		flash("Passwords are not the same.")
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
	new_user.firstName = firstName
	new_user.lastName = lastName
	new_user.username = username
	new_user.email = email
	new_user.password = pword_hash
	try:
		new_user.save()
	except NotUniqueError as e:
		flash(str(e))
		return RegisterStatus.not_unique
	except ValidationError as e:
		flash(str(e))
		return RegisterStatus.bad_validation
	# TODO Login after successful register
	return RegisterStatus.success
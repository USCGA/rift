from flask import Blueprint, render_template, request, escape, session, redirect, url_for
from mongoengine import Document, DoesNotExist, MultipleObjectsReturned
from passlib.hash import pbkdf2_sha256
import rift.nav as nav
import rift.models as models

main = Blueprint("pages", __name__)

@main.route("/")
def index():
	# Check if valid session.
	if 'username' in session:
		login_status = 'Logged in as %s' % escape(session['username'])
	else:
		login_status = 'You are not logged in.'
	menu = nav.items
	return render_template('home.html', menu=menu, Motd=models.Motd, login_status=login_status)

@main.route("/login", methods=['GET','POST'])
def login():
	# Check if valid session.
	if 'username' in session:
		login_status = 'Logged in as %s' % escape(session['username'])
	else:
		login_status = 'You are not logged in.'
	# TODO Add validation to email/uname/pword.
	if request.method == 'POST':
		if request.form['type'] == "login": # ----------- LOGIN
			uname = request.form['uname']
			pword = request.form['pword']
			# Retrieve user from db.
			try:
				user = models.User.objects.get(username=uname)
			except DoesNotExist:
				return uname + " DNE."
			except MultipleObjectsReturned:
				return "Somehow, there is more than \
					one user by the name of " + uname
			# Ensure password match.
			if pbkdf2_sha256.verify(pword, user.password):
				# Good Login.
				# Issue session.
				session['username'] = uname
				return redirect(url_for('pages.index'))
			else:
				# Bad Login.
				# TODO wrong password alert. Will probably involve html/js.
				return "BAD LOGIN, doodsicle"
		elif request.form['type'] == "register": # ------ REGISTER
			# Hash password.
			pword_hash = pbkdf2_sha256.hash(request.form['pword'])
			# Create New User.
			new_user = models.User()
			new_user.email = request.form['email']
			new_user.username = request.form['uname']
			new_user.password = pword_hash
			new_user.save()
			# TODO Login after successful.
		else:
			return "BAD POST, bro."
		return "uname: " + request.form['uname'] + " registered."
	else:
		menu = nav.items
		return render_template('login.html', menu=menu, login_status=login_status)
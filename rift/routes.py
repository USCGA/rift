from flask import Blueprint, render_template, request
from mongoengine import Document, DoesNotExist, MultipleObjectsReturned
from passlib.hash import pbkdf2_sha256
import rift.nav as nav
import rift.models as models

main = Blueprint("pages", __name__)

@main.route("/")
def root():
	menu = nav.items
	return render_template('home.html', menu=menu, Motd=models.Motd)

@main.route("/login", methods=['GET','POST'])
def login():
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
				# TODO issue login token.
				return "GOOD LOGIN, brother."
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
		return render_template('login.html', menu=menu)
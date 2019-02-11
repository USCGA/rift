from flask import Blueprint, render_template, request
from mongoengine import Document
import rift.nav as nav
import rift.models as models

main = Blueprint("pages", __name__)

@main.route("/")
def root():
	menu = nav.items
	return render_template('home.html', menu=menu, Motd=models.Motd)

@main.route("/login", methods=['GET','POST'])
def login():
	if request.method == 'POST':
		return "LOGIN! " + request.authorization['username']
	else:
		menu = nav.items
		return render_template('login.html', menu=menu)
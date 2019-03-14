from flask import Blueprint, render_template, request, \
	escape, session, redirect, url_for, Response, g
from functools import wraps
import rift.nav as nav
import rift.models as models
import rift.user as user

# All routes defined below belong to the "main" blueprint 
# which is applied to flask.app in __init__.py.
main = Blueprint("pages", __name__)


# --- Configuration ---
# Variables we might want to change later.
default_screenname = "guest"

### DECORATORS ###

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('pages.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


### ROUTES ###

# Before each request
@main.before_request
def get_user():
	if 'user' not in g:
		if 'username' in session:
			g.user = user.GetUserObject(session)
			return
		else:
			g.user = None
			return
	else:
		return

# Homepage
@main.route("/")
def home():
	screenname = g.user.username.lower() if g.user is not None else default_screenname
	return render_template(
		'home.html', 
		menu=nav.guest_menu, 
		screenname=screenname)

# Rift Dashboard
@main.route("/dashboard")
@login_required
def dashboard():
	return render_template('rift_dashboard.html', menu=nav.menu_main, user=g.user)

# Login Page
@main.route("/login", methods=['GET','POST'])
def login():
	if g.user is not None:
		return redirect(url_for('pages.dashboard'))
	# POST
	if request.method == 'POST':
		if request.form['type'] == "login": # ----------- LOGIN
			uname = request.form['uname']
			pword = request.form['pword']
			result = user.Login(uname, pword)
			if (result == user.LoginStatus.success):
				return redirect(url_for('pages.dashboard'))
			else:
				return render_template('login.html')
	# GET
	if request.method == 'GET':
		return render_template('login.html')

# Register Page
@main.route("/register", methods=['GET','POST'])
def register():
	if g.user is not None:
		return redirect(url_for('pages.dashboard'))
	# POST
	if request.method == 'POST':
		if request.form['type'] == "register": # ------ REGISTER
			fname = request.form['fname'] # First Name
			lname = request.form['lname'] # Last Name
			uname = request.form['uname'] # Screenname
			email = request.form['email'] # Email Address
			pword = request.form['pword'] # Password
			rpass = request.form['rpass'] # Repeated Password
			result = user.Register(fname, lname, uname, email, pword, rpass)
			if (result == user.RegisterStatus.success):
				return redirect(url_for('pages.dashboard'))
			else:
				return render_template('register.html')

		return render_template('register.html')
	# GET
	if request.method == 'GET':
		return render_template('register.html')

# Logout Page
# No page is actually displayed.
# The browser is redirected and session is cleared.
@main.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('pages.home'))
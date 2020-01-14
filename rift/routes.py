from flask import Blueprint, render_template, request, \
	escape, session, redirect, url_for, Response, g, abort, flash, send_from_directory # TODO Move flash required functions into their own file.
from functools import wraps
from flask import current_app as app
from warnings import warn
import mongoengine.errors
import rift.nav as nav
import rift.models as models
import rift.user as user
# Disabled until connecting to docker service from within container is possible.
# import rift.containers as containers
import rift.uploads as uploads
import rift.permissions as permissions
# import rift.api as api

# All routes defined below belong to the "main" blueprint 
# which is applied to flask.app in __init__.py.
main = Blueprint("page", __name__)


# --- Configuration ---
# Variables we might want to change later.
default_screenname = "guest"

### DECORATORS ###

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('page.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission : permissions.Permission, methods=['GET','POST']):
	def decorated_function(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			if request.method in methods and not user.HasPermission(g.user, permission):
				return "<h3>You do not have permission to "+ request.method +" this.</h3><p>'" + permission.tag + "' permission required.</p>"
			else:
				return f(*args, **kwargs)
		return wrapper
	return decorated_function
### ROUTES ###

# ---------------------- Before Request ----------------------
# Before each request
@main.before_request
def get_user(refresh=False):
	if 'user' not in g:
		if 'username' in session:
			g.user = user.GetUserObject(session)
			return
		else:
			g.user = None
			return
	else:
		# The refresh parameter is necessary if g.user needs 
		# to be updated during a request as well as before.
		if refresh == True:
			g.user = user.GetUserObject(session)
		else:
			return
# ------------------------------------------------------------


# --------------------------- Pages --------------------------
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
	# Retrieve latest announcements
	postsQuerySet = models.Post.objects.order_by('-date').limit(3)
	postsQuerySet = postsQuerySet(_cls='Post.Announcement')

	# Retrieve "Creator" Information
	challengesQuerySet = models.CTFChallenge.objects(author=g.user)

	return render_template('rift_dashboard.html', menu=nav.menu_main, user=g.user, posts=postsQuerySet, challenges=challengesQuerySet)

# Homebrew Page (In house CTF main-page)
@main.route("/ctf", methods=['GET','POST'])
@login_required
@permission_required(permissions.CreateCTFs, methods=['POST'])
def ctfs():
	ctfQuerySet = models.CTF.objects

	canCreate = False
	if (user.HasPermission(g.user, permissions.CreateCTFs)):
		canCreate = True

	# POST
	if request.method == 'POST':
		newCTF = models.CTF()
		newCTF.name = request.form['ctfTitle']
		newCTF.description = request.form['ctfDescription']
		newCTF.author = g.user
		newCTF.save()
	return render_template('rift_ctfs.html', menu=nav.menu_main, user=g.user, ctfs=ctfQuerySet, canCreate = canCreate)

# Rift Single CTF Page
@main.route("/ctf/<id>", methods=['GET','POST'])
@login_required
def ctf(id):
	try:
		ctf = models.CTF.objects.get(id=id)
		challenges = models.CTFChallenge.objects(ctf=ctf)
	except:
		abort(404)

	canEdit = False

	# Enable/Disable Edit Controls
	if (user.HasCTFOwnership(g.user, id) or user.HasPermission(g.user, permissions.ModerateCTFs)):
		canEdit = True

	# GET
	if request.method == 'GET':
		deleteArg = request.args.get('delete', default = False, type = bool)
		# TODO: Add admin delete perms
		if (deleteArg == True):
			if (canEdit):
				ctf.delete()
				return redirect(url_for('page.ctfs'))
			else:
				abort(403)

	# POST
	if request.method == 'POST':
		if (user.HasCTFOwnership(g.user,id) or user.HasPermission(g.user, permissions.ModerateCTFs)):
			ctf.name = request.form['ctfName']
			ctf.description = request.form['ctfDescription']
			ctf.save()
		else:
			abort(403)
	
	return render_template('rift_ctf.html', menu=nav.menu_main, user=g.user, ctf=ctf, challenges=challenges, canEdit=canEdit)

# Rift Challenge Editor
@main.route("/chedit", methods=['GET','POST'])
@login_required
@permission_required(permissions.CreateCTFs)
def challenge_editor():
	ctfs = models.CTF.objects(author=g.user).only('name')
	challenge_id = request.args.get('id')

	if (request.referrer != None):
		cancelURL = request.referrer
	else:
		cancelURL = url_for('page.dashboard')

	# Retrieve challenge if it exists already.
	if (challenge_id is not None):
		try:
			challengeDocument = models.CTFChallenge.objects.get(id=challenge_id)
			if challengeDocument.filename is not None:
				file_url = uploads.ctf_files.url(challengeDocument.filename)
			else:
				file_url = None
		except:
			abort(404)
	else:
		challengeDocument = models.CTFChallenge()

	# Abort if there is an owner and the user isn't one.
	if (g.user == challengeDocument.author or challengeDocument.author == None):
		pass
	elif (user.HasPermission(g.user, permissions.ModerateCTFs)):
		flash("You are editing this challenge as an administrator.")
		ctfs = models.CTF.objects.only('name')
	else:
		abort(403)

	# POST
	if request.method == 'POST':
		challengeDocument.title = request.form['challengeTitle']
		challengeDocument.description = request.form['challengeDescription']
		if (challengeDocument.author == None): challengeDocument.author = g.user
		challengeDocument.category = request.form['challengeCategory']
		challengeDocument.flag = request.form['challengeFlag']
		if (user.HasCTFOwnership(g.user, request.form['ctf']) or user.HasPermission(g.user, permissions.ModerateCTFs)):
			challengeDocument.ctf = models.CTF.objects.get(id=request.form['ctf'])
		else:
			abort(403)
		challengeDocument.point_value = request.form['challengePointValue']
		if 'challengeFile' in request.files:
			if request.files['challengeFile'].filename != '':
				filename = uploads.ctf_files.save(request.files['challengeFile'])
				challengeDocument.filename = filename
		challengeDocument.save()
		return redirect(url_for('page.challenge',id=challengeDocument.id))
	return render_template('rift_challenge_editor.html', challenge=challengeDocument, menu=nav.menu_main, user=g.user, ctfs=ctfs, cancelURL=cancelURL)

# Rift Single Challenge Page
@main.route("/challenges/<id>", methods=['GET','POST'])
@login_required
def challenge(id):
	try:
		challengeDocument = models.CTFChallenge.objects.get(id=id)
		if challengeDocument.filename is not None:
			file_url = uploads.ctf_files.url(challengeDocument.filename)
		else:
			file_url = None
	except:
		abort(404)

	canEdit = False
	# Enable/Disable Edit Controls
	if (g.user == challengeDocument.author or user.HasCTFOwnership(g.user, challengeDocument.ctf.id) or user.HasPermission(g.user, permissions.ModerateCTFs)):
		canEdit = True
	
	# GET
	if request.method == 'GET':
		deleteArg = request.args.get('delete', default = False, type = bool)
		if (deleteArg == True):
			if (canEdit):
				if challengeDocument.filename != None:
					uploads.Delete(uploads.ctf_files, challengeDocument.filename)
				challengeDocument.delete()
				return redirect(url_for('page.ctf', id=challengeDocument.ctf.id))
			else:
				abort(403)
	# POST
	if request.method == 'POST':
		if ('flagSubmission' in request.form):
			submittedFlag = request.form['flag']
			if (submittedFlag == challengeDocument.flag):
				# Score Flag
				user.ScoreChallenge(g.user, challengeDocument)
				# Update g.user before the page is displayed again.
				get_user(refresh=True)
	return render_template('rift_challenge.html', menu=nav.menu_main, user=g.user, challenge=challengeDocument, file_url=file_url, canEdit=canEdit)

# Rift Scoreboard Page
@main.route("/scoreboard")
@login_required
def scoreboard():
	scoreboardUserDocuments = models.User.objects
	return render_template('rift_scoreboard.html', menu=nav.menu_main, user=g.user, scoreboard_users=scoreboardUserDocuments)

# Rift Profile Page
@main.route("/profile")
@login_required
def profile():
	return render_template('rift_profile.html', menu=nav.menu_main, user=g.user)

# Download
@main.route("/uploads/<path:filename>")
def download(filename):
	return send_from_directory(app.config['UPLOADS_DEFAULT_DEST'], filename)

# Login Page
@main.route("/login", methods=['GET','POST'])
def login():
	if g.user is not None:
		return redirect(url_for('page.dashboard'))
	# POST
	if request.method == 'POST':
		if request.form['type'] == "login": # ----------- LOGIN
			uname = request.form['uname']
			pword = request.form['pword']
			result = user.Login(uname, pword)
			if (result == user.LoginStatus.success):
				return redirect(url_for('page.dashboard'))
			else:
				return render_template('login.html')
	# GET
	if request.method == 'GET':
		return render_template('login.html')

# Register Page
@main.route("/register", methods=['GET','POST'])
def register():
	if g.user is not None:
		return redirect(url_for('page.dashboard'))
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
				return redirect(url_for('page.dashboard'))
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
	return redirect(url_for('page.home'))

@main.route("/admin/status")
def rift_status():
	return render_template('rift_status.html', menu=nav.menu_main, user=g.user, mongo_isRunning="Not Implemented", containers=["Not Implemented"])

# Rift Admin User Page
# TODO: This is neigh unreadable. There must be a better way to go about this.
@main.route("/admin/users", methods=['GET','POST'])
@login_required
@permission_required(permissions.EditUserRoles)
def rift_users():
	userDocuments = models.User.objects
	roles = []
	for k in permissions.Role.List():
		if k == permissions.Role.Get("Admin"): continue
		roles.append(k)
	if request.method == 'POST':
		for key in request.form:
			newRole = request.form[key]
			if newRole in roles:
				userDocuments.get(id=key).update(role=newRole)
			else:
				warn(g.user.username + " attempted to set " + userDocuments.get(id=key).username + "'s role to " + newRole + " which doesn't exist.", UserWarning, stacklevel=2)
		print("[!] User permissions updated by " + g.user.username)
	return render_template('rift_admin_users.html', menu=nav.menu_main, user=g.user, users=userDocuments, roles=roles)

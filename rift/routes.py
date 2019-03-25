from flask import Blueprint, render_template, request, \
	escape, session, redirect, url_for, Response, g
from functools import wraps
import rift.nav as nav
import rift.models as models
import rift.user as user

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
	# Retrieve latest announcements
	postsQuerySet = models.Post.objects.order_by('-date').limit(3)
	return render_template('rift_dashboard.html', menu=nav.menu_main, user=g.user, posts=postsQuerySet)

# Rift Posts Page
@main.route("/posts", methods=['GET','POST'])
@login_required
def posts():
	postsQuerySet = models.Post.objects.order_by('-date')
	authorArg = request.args.get('author', type = str)
	if authorArg is not None:
		try:
			# We have to try here, because specified user might not exist.
			selAuthor = models.User.objects.get(username=authorArg)
			postsQuerySet = postsQuerySet(author=selAuthor)
		except:
			postsQuerySet = []

	# POST
	if request.method == 'POST':
		newPost = models.Post()
		newPost.author = g.user
		newPost.title = request.form['postTitle']
		newPost.content = request.form['postContent']
		newPost.save()
	return render_template('rift_posts.html', menu=nav.menu_main, user=g.user, posts=postsQuerySet)

# Rift Writeups Page
@main.route("/writeups", methods=['GET','POST'])
@login_required
def writeups():
	collections = models.WriteupCollection.objects
	writeupQuerySet = models.Writeup.objects.order_by('-date')
	authorArg = request.args.get('author', type = str)
	if authorArg is not None:
		try:
			# We have to try here, because specified user might not exist.
			selAuthor = models.User.objects.get(username=authorArg)
			writeupQuerySet = writeupQuerySet(author=selAuthor)
		except:
			writeupQuerySet = []

	# POST
	if request.method == 'POST':
		newWriteup = models.Writeup()
		newWriteup.author = g.user
		newWriteup.title = request.form['writeupTitle']
		newWriteup.content = request.form['writeupContent']
		newWriteup.collection = models.WriteupCollection.objects.get(id=request.form['writeupCollection'])
		newWriteup.save()
	return render_template('rift_writeups.html', menu=nav.menu_main, user=g.user, posts=writeupQuerySet, collections=collections)

# Rift Writeup Collections
# TODO this is currently unimplemented
@main.route("/writeups/collections", methods=['GET','POST'])
@login_required
def writeup_collections():
	collectionQuerySet = models.WriteupCollection.objects

	# POST
	if request.method == 'POST':
		newCollection = models.WriteupCollection()
		newCollection.name = request.form['collectionTitle']
		newCollection.link = request.form['collectionLink']
		newCollection.save()
	return render_template('rift_writeupcollections.html', menu=nav.menu_main, user=g.user, collections=collectionQuerySet)

# Rift Single Post Page
@main.route("/posts/<id>", methods=['GET','POST'])
@login_required
def post(id):
	postDocument = models.Post.objects.get(id=id)
	# GET
	if request.method == 'GET':
		deleteArg = request.args.get('delete', default = False, type = bool)
		# User must be the document's author to delete. #TODO Add admin perms
		if (deleteArg == True and g.user == postDocument.author):
			postDocument.delete()
			return redirect(url_for('page.posts'))
	# POST
	if request.method == 'POST':
		# User must be the document's author to edit. #TODO Add admin perms
		if (g.user == postDocument.author):
			postDocument.title = request.form['postTitle']
			postDocument.content = request.form['postContent'] #TODO Display formatted markdown
			postDocument.save()
	return render_template('rift_post.html', menu=nav.menu_main, user=g.user, post=postDocument)

# Rift Profile Page
@main.route("/profile")
@login_required
def profile():
	return render_template('rift_profile.html', menu=nav.menu_main, user=g.user)

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
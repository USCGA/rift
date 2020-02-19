import os
from flask import Flask, render_template, Markup, session
from flask_misaka import Misaka
from rift.routes import main
import flask_uploads
import rift.db
#import rift.containers
import rift.uploads
import secrets

app = Flask(__name__)
db = rift.db.connection(debug=app.debug)

# Enable the Misaka extension. (Markdown Parser)
Misaka(app)

# Configure Uploads
app.config['UPLOADS_DEFAULT_DEST'] = os.path.dirname(os.path.realpath(__file__)) + "/uploads"
flask_uploads.configure_uploads(app, (rift.uploads.ctf_files, rift.uploads.images))

# App Configuration
app.jinja_env.line_statement_prefix = '%'
app.config['MAX_CONTENT_LENGTH'] = 2 * 16 * 1024 * 1024 # 32 Megabytes
app.config['INVITE_CODE_REQUIRED'] = True
app.config['INVITE_CODE'] = secrets.token_hex(16)
if app.debug:
	app.config['SECRET_KEY'] = "replaceme"
	print("[i] Invite Code: %s" % app.config['INVITE_CODE'])
else:
	app.config['SECRET_KEY'] = secrets.token_hex(16)

# Configure Routes
app.register_blueprint(main)

# ---------------------- Error Handlers ----------------------
# 400
@app.errorhandler(400)
def page_not_found(e):
	# note that we set the 400 status explicitly
	return "400 ?:(", 400

# 403
@app.errorhandler(403)
def page_forbidden(e):
	# note that we set the 401 status explicitly
	return "401 >:(", 403

# 404
@app.errorhandler(404)
def page_not_found(e):
	# note that we set the 404 status explicitly
	return "404 :(", 404
# ------------------------------------------------------------

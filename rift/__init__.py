import os
from flask import Flask, render_template, Markup, session
from flask_misaka import Misaka
from rift.routes import main
import flask_uploads
import rift.db
import rift.containers
import rift.uploads
import secrets

app = Flask(__name__)
db = rift.db.connection

# Enable the Misaka extension. (Markdown Parser)
Misaka(app)

# Configure Uploads
app.config['UPLOADS_DEFAULT_DEST'] = os.path.dirname(os.path.realpath(__file__)) + "/uploads"
flask_uploads.configure_uploads(app, (rift.uploads.ctf_files, rift.uploads.images))

# Read/Generate secret key.
try:
	f = open("secret.key", 'r')
	app.secret_key = f.read()
	f.close()
except FileNotFoundError:
	g = open("secret.key", 'w')
	app.secret_key = secrets.token_hex(16)
	g.write(app.secret_key)
	g.close
except:
	print("[x] Something has gone wrong reading/writing the app.secret_key. Check file permissions.")
	raise

# App Configuration
app.jinja_env.line_statement_prefix = '%'
app.config['DEBUG'] = True
app.config['MAX_CONTENT_LENGTH'] = 2* 16 * 1024 * 1024 # 32 Megabytes

# MongoDB Config
app.config['MONGODB_DB'] = 'rift'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# Configure Routes
app.register_blueprint(main)
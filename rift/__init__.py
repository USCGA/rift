from flask import Flask, render_template, Markup
from rift.routes import main
from rift.models import Motd
import rift.db


app = Flask(__name__)
db = rift.db.connection

# App Configuration
app.jinja_env.line_statement_prefix = '%'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'salt'

# MongoDB Config
app.config['MONGODB_DB'] = 'rift'
app.config['MONGODB_HOST'] = 'localhost'
app.config['MONGODB_PORT'] = 27017

# Configure Routes
app.register_blueprint(main)
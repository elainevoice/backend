from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask('project')
app.config['SECRET_KEY'] = 'very-secret'
app.debug = True
toolbar = DebugToolbarExtension(app)

from app import routes

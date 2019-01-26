from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)
from .models import User, Voting, Vote, Alternative
db.create_all()

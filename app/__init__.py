import functools

from flask import Flask, g, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_pyfile('../config.py')
db = SQLAlchemy(app)
from .models import User, Voting, Vote, Alternative
db.create_all()


def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        load_logged_in_user()
        if g.user == None:
            return redirect(url_for('login'))

        return view(**kwargs)
    return wrapped_view

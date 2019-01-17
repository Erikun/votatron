import functools

from flask import Blueprint, request, redirect, flash, render_template, session, g, url_for

from . import app
from .movie import movie


app.register_blueprint(movie, url_prefix="/movie")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        load_logged_in_user()
        if g.user == None:
            return redirect(url_for('login'))

        return view(**kwargs)
    return wrapped_view


@app.route('/register', methods = ('GET', 'POST'))
def register():
    return "register"


@app.route('/login', methods = ('GET', 'POST'))
def login():
    return render_template('auth/login.html')


@app.route('/index')
@login_required
def index():
    return "index"


def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id

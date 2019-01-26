import functools

from flask import Blueprint, request, redirect, flash, render_template, session, g, url_for

from . import app, db
from .movie import movie
from .models import User


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
    if request.method == 'GET':
        return render_template('auth/register.html')
    else:
        username = request.form['username']
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = username
        flash("logged in as " + username)
        return(redirect(url_for('index')))


@app.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("no such user")
            return(redirect(url_for('register')))
        else:
            flash("logged in")
            session['user_id'] = username
            return(redirect(url_for('index')))


@app.route('/logout', methods = ('GET', 'POST'))
def logout():
    return "logout"


@app.route('/index')
@login_required
def index():
    return render_template('base.html')


def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id

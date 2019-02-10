import functools

from flask import Blueprint, request, redirect, flash, render_template, session, g, url_for

from . import app, db, login_required
from .movie import movie
from .models import User
from .poll import poll
from .nominate import nominate
from .vote import vote


app.register_blueprint(movie, url_prefix="/movie")
app.register_blueprint(poll, url_prefix="/poll")
app.register_blueprint(nominate, url_prefix="/nominate")
app.register_blueprint(vote, url_prefix="/vote")


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
            flash("No such user")
            return(redirect(url_for('register')))
        else:
            flash("Logged in as " + username)
            session['user_id'] = username
            return(redirect(url_for('index')))


@app.route('/logout', methods = ('GET', 'POST'))
def logout():
    g.user = None
    session.clear()
    return(redirect(url_for('index')))


@app.route('/')
@login_required
def index():
    return (redirect(url_for('poll.list_polls')))

"""
Blueprint to show or create votings.
"""

from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for

from . import login_required, db
from .models import Poll, User, Alternative, Vote


poll = Blueprint('poll', __name__, template_folder='templates')


@poll.route('/', methods=["GET"])
@login_required
def list_polls():
    "Show all pllls"
    user = db.session.query(User).filter(User.username == g.user).one()
    created_polls = user.polls
    nominated_polls = (db.session.query(Poll)
                       .join(Alternative)
                       .filter(Alternative.poll_id == Poll.id)
                       .filter(Alternative.creator == user.username)
                       .all())
    voted_polls = (db.session.query(Poll)
                   .join(Vote)
                   .filter(Vote.poll_id == Poll.id)
                   .filter(user.username == Vote.username)).all()
    return render_template('polls.html.jinja2',
                           created_polls=created_polls,
                           nominated_polls=nominated_polls,
                           voted_polls=voted_polls)


@poll.route('/show/<uuid:poll_id>', methods=["GET"])
@login_required
def show_poll(poll_id):
    "Display the current state of a single poll"
    poll = db.session.query(Poll).filter(Poll.id == str(poll_id)).one()
    now = datetime.now()
    if poll.is_nominating(now):
        return render_template('poll_nominating.html.jinja2', poll=poll)


@poll.route('/create', methods=["GET", "POST"])
@login_required
def create_poll():
    "Create a new poll"
    if request.method == "GET":
        return render_template('create_poll.html.jinja2')
    else:
        data = request.form
        poll = Poll(title=data["title"], creator=g.user)
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for('poll.show_poll', poll_id=poll.id))

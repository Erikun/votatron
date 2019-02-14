"""
Blueprint to show or create votings.
"""

from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for, flash

from . import login_required, db
from .models import Poll, User, Alternative, Vote

import json


poll = Blueprint('poll', __name__, template_folder='templates')


@poll.route('/', methods=["GET"])
@login_required
def list_polls():
    "Show all polls"
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
    poll_url = request.url
    now = datetime.now()
    if poll.is_nominating(now):
        return render_template('poll_nominating.html.jinja2', poll=poll, poll_url=poll_url)
    if poll.is_voting(now):
        if poll.has_voted(g.user):
            return render_template('poll_voting.html.jinja2', poll=poll, poll_url=poll_url)
        return redirect(url_for('vote.cast', poll_id=poll.id))
    else:
        alternatives = db.session.query(Alternative).filter(Alternative.poll_id == str(poll_id)).order_by(Alternative.score.desc()).all()
        return render_template('poll_result.html.jinja2', poll=poll, alternatives=alternatives, poll_url=poll_url)


@poll.route('/create', methods=["GET", "POST"])
@login_required
def create_poll():
    "Create a new poll"
    if request.method == "GET":
        return render_template('create_poll.html.jinja2')
    else:
        data = request.form
        if len(data['title']) == 0:
            flash("You must have a title for the poll.")
            return render_template('create_poll.html.jinja2')
        config = {"type": data['type']}
        poll = Poll(title=data["title"], creator=g.user,
                    config=json.dumps(config))
        db.session.add(poll)
        db.session.commit()
        return redirect(url_for('poll.show_poll', poll_id=poll.id))


@poll.route('/<uuid:poll_id>/start', methods=["POST"])
@login_required
def start_vote(poll_id):
    poll = db.session.query(Poll).filter(Poll.id == str(poll_id)).one()
    now = datetime.now()
    assert poll.is_nominating(now), "Vote has already been started."
    poll.voting_start = now
    db.session.commit()
    return redirect(url_for('vote.cast', poll_id=poll.id))


@poll.route('/<uuid:poll_id>/end', methods=["POST"])
@login_required
def end_vote(poll_id):
    poll = db.session.query(Poll).filter(Poll.id == str(poll_id)).one()
    now = datetime.now()
    assert poll.is_voting(now), "Can't end vote that is not ongoing."
    poll.voting_end = now
    db.session.commit()
    return redirect(url_for('poll.show_poll', poll_id=poll.id))

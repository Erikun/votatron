"""
Blueprint to vote in a poll.
"""

from datetime import datetime

from flask import Blueprint, render_template, request, g, redirect, url_for, abort

from . import login_required, db
from .models import Poll, Vote


vote = Blueprint('vote', __name__, template_folder='templates')


@vote.route('/<uuid:poll_id>', methods=["GET", "POST"])
@login_required
def cast(poll_id):
    poll = db.session.query(Poll).get(str(poll_id))
    now = datetime.now()
    assert poll.is_voting(now), "Sorry, voting is not open for this poll."
    if request.method == "GET":
        return render_template("vote.html.jinja2", poll=poll)
        
    data = request.form

    if poll.has_voted(g.user):
        return redirect('poll.show_poll', poll_id=poll.id)

    vote = Vote(username=g.user, poll_id=poll.id)
    db.session.add(vote)
    for alternative in poll.alternatives:
        score = int(data.get(str(alternative.id), 0))
        alternative.score += score
    db.session.commit()
    return redirect(url_for('poll.show_poll', poll_id=poll.id))
        
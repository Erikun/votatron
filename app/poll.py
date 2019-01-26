"""
Blueprint to show or create votings.
"""

from flask import Blueprint, render_template, request, g, redirect, url_for

from . import login_required, db
from .models import Poll


poll = Blueprint('poll', __name__, template_folder='templates')


@poll.route('/', methods=["GET"])
def index():
    "Show all pllls"
    return render_template('polls.html.jinja2', polls=db.session.query(Poll).all())


@poll.route('/show/<uuid:poll_id>', methods=["GET"])
def show_poll(poll_id):
    "Display the current state of a single poll"
    # TBD


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

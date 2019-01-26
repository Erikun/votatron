"""
Blueprint to show or create votings.
"""

from flask import Blueprint, render_template, request, g, redirect, url_for

from . import login_required, db
from .models import Voting


voting = Blueprint('voting', __name__, template_folder='templates')


@voting.route('/', methods=["GET"])
def index():
    "Show all votings"
    return render_template('votings.html.jinja2', votings=db.session.query(Voting).all())


@voting.route('/show/<uuid:voting_id>', methods=["GET"])
def show_voting(voting_id):
    "Display the current state of a single voting"
    # TBD


@voting.route('/create', methods=["GET", "POST"])
@login_required
def create_voting():
    "Create a new voting"
    if request.method == "GET":
        return render_template('create_voting.html.jinja2')
    else:
        data = request.form
        voting = Voting(title=data["title"], creator=g.user)
        db.session.add(voting)
        db.session.commit()
        return redirect(url_for('voting.show_voting', voting_id=voting.id))

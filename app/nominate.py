"""
Blueprint to nominate alternatives for polls.
"""

from flask import Blueprint, render_template, request, g, redirect, url_for

from . import login_required, db
from .models import Poll, Alternative


nominate = Blueprint('nominate', __name__, template_folder='templates')


@nominate.route('/<uuid:poll_id>', methods=["GET", "POST", "DELETE"])
@login_required
def nominate_alternative(poll_id):
    if request.method == "GET":
        poll = db.session.query(Poll).filter(Poll.id == str(poll_id)).one()
        return render_template('nominate.html.jinja2', poll=poll)
    elif request.method == "POST":
        data = request.form
        # Since browsers won't allow DELETE method on forms, we'll hack it instead
        delete = data.get("delete")
        if delete:
            alternative_id = data.get("alternative")
            alternative = db.session.query(Alternative).filter(Alternative.id == alternative_id).one()
            db.session.delete(alternative)
        else:
            title = data.get("title")
            link = data.get("link")
            alternative = Alternative(title=title, link=link,
                                      creator=g.user, poll_id=str(poll_id))
            db.session.add(alternative)
        db.session.commit()
        return redirect(url_for('poll.show_poll', poll_id=poll_id))



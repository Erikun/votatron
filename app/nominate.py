"""
Blueprint to nominate alternatives for polls.
"""

from flask import Blueprint, render_template, request, g, redirect, url_for

from . import login_required, db
from .models import Poll, User, Alternative


nominate = Blueprint('nominate', __name__, template_folder='templates')


@nominate.route('/<uuid:poll_id>', methods=["GET", "POST"])
@login_required
def nominate_alternatives(poll_id):
    if request.method == "GET":
        user = db.session.query(User).filter(User.username == g.user).one()
        poll = db.session.query(Poll).filter(Poll.id == str(poll_id)).one()
        alternatives = []
        alternatives = (db.session.query(Alternative)
                        .filter(Alternative.poll_id == str(poll_id))
                        .filter(Alternative.creator == user.username)
                        .all())
        return render_template('nominate.html.jinja2',
                                alternatives=alternatives,
                                poll_id=poll_id)
    else:
        data = request.form
        alt_titles = data.getlist("title")
        alt_links = data.getlist("link")
        if "id" in request.form:
            alt_id = data.getlist("id")
            for i in range(len(alt_id)):
                alternative = Alternative.query.get(alt_id[i])
                alternative.title = alt_titles[i]
                alternative.link = alt_links[i]
                db.session.commit()
        else:
            for i in range(len(alt_titles)):
                alternative = Alternative(title=alt_titles[i], creator=g.user
                                    , poll_id=str(poll_id), link=alt_links[i])
                db.session.add(alternative)
                db.session.commit()
        return redirect(url_for('nominate.nominate_alternatives', poll_id=poll_id))

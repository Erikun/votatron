from flask import Blueprint, render_template, request

from .movie_search import find_movie


movie = Blueprint('movie', __name__, template_folder='templates')


@movie.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # User has not searched yet
        return render_template('movie.html.jinja2')
    else:
        # User has entered a search string
        search_string = request.form["search"]
        hits = find_movie("title.basics.tsv", search_string)
        return render_template("movie.html.jinja2", hits=hits)

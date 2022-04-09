from flask import render_template, request
from flask_user import login_required

from quizzes.app import app


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz")
@login_required
def choose_quiz_difficulty():
    return render_template("choose_quiz_difficulty.html")


@app.route("/quiz/:difficulty")
@login_required
def take_quiz():

    raise NotImplementedError(request.method)

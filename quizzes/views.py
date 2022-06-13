import itertools
import uuid

import flask
from flask import blueprints, templating, helpers
import flask_user
import flask_login
import requests

from quizzes import models, forms

blueprint = blueprints.Blueprint("quizzes", __name__)


@blueprint.route("/")
def index():
    return templating.render_template("index.html")


@blueprint.route("/quiz")
@flask_user.login_required
def choose_quiz_difficulty():
    return templating.render_template("choose_quiz_difficulty.html")


@blueprint.route("/quiz/prepare/<difficulty>")
@flask_user.login_required
def prepare_quiz(difficulty: str):
    api_response = requests.get(f"https://opentdb.com/api.php?amount=10&difficulty={difficulty}")
    questions = api_response.json()["results"]
    quiz_uuid = uuid.uuid4().hex
    quiz_taken = models.QuizTaken(
        uuid=quiz_uuid,
        difficulty=difficulty,
        questions=[
            models.QuizQuestion(
                question=q["question"],
                correct_answer=q["correct_answer"],
                incorrect_answers=q["incorrect_answers"],
            )
            for q in questions
        ],
    )
    models.fake_db.quizzes_taken[quiz_uuid] = quiz_taken
    return flask.redirect(helpers.url_for("quizzes.take_quiz", quiz_uuid=quiz_uuid))


@blueprint.route("/quiz/take/<quiz_uuid>", methods=["GET", "POST"])
@flask_user.login_required
def take_quiz(quiz_uuid: str):
    try:
        quiz_taken = models.fake_db.quizzes_taken[quiz_uuid]
    except KeyError:
        return flask.redirect(helpers.url_for("quizzes.choose_quiz_difficulty"))

    Form = forms.quiz_form_factory(quiz_taken)
    if flask.request.method == "GET":
        return templating.render_template("take_quiz.html", form=Form())
    else:
        form = Form(flask.request.form)
        if form.validate():
            points = models.calculate_points(quiz_taken, flask.request.form)
            models.fake_db.quiz_results[flask_login.current_user.id].append(
                models.QuizResult(user_id=flask_login.current_user.id, quiz_uuid=quiz_taken.uuid, points=points)
            )
            return flask.redirect(helpers.url_for("quizzes.ranking"))
        return templating.render_template("take_quiz.html", form=form)


@blueprint.route("/ranking")
def ranking():
    quiz_results_sorted = sorted(
        itertools.chain(*models.fake_db.quiz_results.values()), key=lambda qr: qr.points, reverse=True
    )
    return templating.render_template("ranking.html", ranking=quiz_results_sorted)


@blueprint.route("/ranking.json")
def ranking_json():
    quiz_results_sorted = sorted(
        itertools.chain(*models.fake_db.quiz_results.values()), key=lambda qr: qr.points, reverse=True
    )
    return {"ranking": quiz_results_sorted}

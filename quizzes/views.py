import uuid

import flask
from flask import blueprints, templating, helpers
import flask_user
import flask_login
import requests
from sqlalchemy.orm import exc as orm_exceptions

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

    quiz = models.Quiz(difficulty=models.QuizDifficulty[difficulty.upper()])
    models.db.session.add(quiz)
    for q in questions:
        quiz.quiz_questions.append(
            models.QuizQuestion(
                question=q["question"],
                correct_answer=q["correct_answer"],
                incorrect_answers=q["incorrect_answers"],
            )
        )
    models.db.session.commit()

    return flask.redirect(helpers.url_for("quizzes.take_quiz", quiz_id=quiz.id))


@blueprint.route("/quiz/take/<quiz_id>", methods=["GET", "POST"])
@flask_user.login_required
def take_quiz(quiz_id: int):
    try:
        quiz = models.db.session.query(models.Quiz).filter(models.Quiz.id == quiz_id).one()
    except orm_exceptions.NoResultFound:
        return flask.redirect(helpers.url_for("quizzes.choose_quiz_difficulty"))

    Form = forms.quiz_form_factory(quiz)
    if flask.request.method == "GET":
        return templating.render_template("take_quiz.html", form=Form())
    else:
        form = Form(flask.request.form)
        if form.validate():
            points = models.calculate_points(quiz, flask.request.form)
            models.db.session.add(models.QuizResult(user=flask_login.current_user, quiz=quiz, points=points))
            models.db.session.commit()
            return flask.redirect(helpers.url_for("quizzes.ranking"))
        return templating.render_template("take_quiz.html", form=form)


@blueprint.route("/ranking")
def ranking():
    quiz_results = models.db.session.query(models.QuizResult).order_by(models.QuizResult.points.desc())
    return templating.render_template("ranking.html", ranking=quiz_results)


@blueprint.route("/ranking.json")
def ranking_json():
    quiz_results = models.db.session.query(models.QuizResult).order_by(models.QuizResult.points.desc())
    return {
        "ranking": [
            {
                "user": {
                    "username": r.user.username,
                },
                "quiz": {
                    "id": r.quiz.id,
                },
                "points": r.points,
            }
            for r in quiz_results
        ]
    }

from itertools import chain
from uuid import uuid4

from flask import render_template, request, redirect, url_for, Blueprint
from flask_login import current_user
from flask_user import login_required
from requests import get

from quizzes.forms import quiz_form_factory
from quizzes.models import QuizTaken, QuizQuestion, calculate_points, QuizResult, fake_db

blueprint = Blueprint("quizzes", __name__)


@blueprint.route("/")
def index():
    return render_template("index.html")


@blueprint.route("/quiz")
@login_required
def choose_quiz_difficulty():
    return render_template("choose_quiz_difficulty.html")


@blueprint.route("/quiz/prepare/<difficulty>")
@login_required
def prepare_quiz(difficulty: str):
    api_response = get(f"https://opentdb.com/api.php?amount=10&difficulty={difficulty}")
    questions = api_response.json()["results"]
    uuid = uuid4().hex
    quiz_taken = QuizTaken(
        uuid=uuid,
        difficulty=difficulty,
        questions=[
            QuizQuestion(
                question=q["question"],
                correct_answer=q["correct_answer"],
                incorrect_answers=q["incorrect_answers"],
            )
            for q in questions
        ],
    )
    fake_db.quizzes_taken[uuid] = quiz_taken
    return redirect(url_for("quizzes.take_quiz", uuid=uuid))


@blueprint.route("/quiz/take/<uuid>", methods=["GET", "POST"])
@login_required
def take_quiz(uuid: str):
    try:
        quiz_taken = fake_db.quizzes_taken[uuid]
    except KeyError:
        return redirect(url_for("quizzes.choose_quiz_difficulty"))

    Form = quiz_form_factory(quiz_taken)
    if request.method == "GET":
        return render_template("take_quiz.html", form=Form())
    else:
        form = Form(request.form)
        if form.validate():
            points = calculate_points(quiz_taken, request.form)
            fake_db.quiz_results[current_user.id].append(
                QuizResult(user_id=current_user.id, quiz_uuid=quiz_taken.uuid, points=points)
            )
            return redirect(url_for("quizzes.ranking"))
        return render_template("take_quiz.html", form=form)


@blueprint.route("/ranking")
def ranking():
    quiz_results_sorted = sorted(chain(*fake_db.quiz_results.values()), key=lambda qr: qr.points, reverse=True)
    return render_template("ranking.html", ranking=quiz_results_sorted)


@blueprint.route("/ranking.json")
def ranking_json():
    quiz_results_sorted = sorted(chain(*fake_db.quiz_results.values()), key=lambda qr: qr.points, reverse=True)
    return {"ranking": quiz_results_sorted}

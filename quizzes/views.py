from itertools import chain
from uuid import uuid4

from flask import render_template, request, redirect, url_for
from flask_login import current_user
from flask_user import login_required
from requests import get

from quizzes.app import app
from quizzes.forms import quiz_form_factory
from quizzes.models import QuizTaken, QuizQuestion, quizzes_taken, calculate_points, QuizResult, quiz_results


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/quiz")
@login_required
def choose_quiz_difficulty():
    return render_template("choose_quiz_difficulty.html")


@app.route("/quiz/prepare/<difficulty>")
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
    quizzes_taken[uuid] = quiz_taken
    return redirect(url_for(".take_quiz", uuid=uuid))


@app.route("/quiz/take/<uuid>", methods=["GET", "POST"])
@login_required
def take_quiz(uuid: str):
    try:
        quiz_taken = quizzes_taken[uuid]
    except KeyError:
        return redirect(url_for(".choose_quiz_difficulty"))

    Form = quiz_form_factory(quiz_taken)
    if request.method == "GET":
        return render_template("take_quiz.html", form=Form())
    else:
        form = Form(request.form)
        if form.validate():
            points = calculate_points(quiz_taken, request.form)
            quiz_results[current_user.id].append(
                QuizResult(user_id=current_user.id, quiz_uuid=quiz_taken.uuid, points=points)
            )
            return redirect(url_for("ranking"))
        return render_template("take_quiz.html", form=form)


@app.route("/ranking")
def ranking():
    quiz_results_sorted = sorted(chain(*quiz_results.values()), key=lambda qr: qr.points, reverse=True)
    return render_template("ranking.html", ranking=quiz_results_sorted)

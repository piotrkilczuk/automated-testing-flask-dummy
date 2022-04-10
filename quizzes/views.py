from uuid import uuid4

from flask import render_template, request, redirect, url_for
from flask_user import login_required
from requests import get

from quizzes.app import app
from quizzes.forms import quiz_form_factory
from quizzes.models import QuizTaken, QuizQuestion, quizzes_taken


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
            return redirect("/")
        return render_template("take_quiz.html", form=form)

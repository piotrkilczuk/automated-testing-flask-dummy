from html import unescape
from typing import Type

from wtforms import Form, RadioField

from quizzes.models import QuizTaken


def quiz_form_factory(quiz_taken: QuizTaken) -> Type[Form]:
    return type(
        "QuizForm",
        (Form,),
        {
            f"question_{i}": RadioField(unescape(q.question), choices=q.incorrect_answers + [q.correct_answer])
            for i, q in enumerate(quiz_taken.questions, start=1)
        },
    )

import html
from typing import Type

import wtforms

from quizzes import models


def quiz_form_factory(quiz_taken: models.Quiz) -> Type[wtforms.Form]:
    quiz_taken.quiz_questions.sort(key=lambda q: q.id)
    return type(
        "QuizForm",
        (wtforms.Form,),
        {
            f"question_{i}": wtforms.RadioField(
                html.unescape(q.question), choices=q.incorrect_answers + [q.correct_answer]
            )
            for i, q in enumerate(quiz_taken.quiz_questions, start=1)
        },
    )

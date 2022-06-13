import html
from typing import Type

import wtforms

from quizzes import models


def quiz_form_factory(quiz_taken: models.QuizTaken) -> Type[wtforms.Form]:
    return type(
        "QuizForm",
        (wtforms.Form,),
        {
            f"question_{i}": wtforms.RadioField(
                html.unescape(q.question), choices=q.incorrect_answers + [q.correct_answer]
            )
            for i, q in enumerate(quiz_taken.questions, start=1)
        },
    )

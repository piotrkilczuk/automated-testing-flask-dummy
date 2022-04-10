from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict

from flask_user import UserMixin

from quizzes.app import db


POINTS_MULTIPLIER = {
    "easy": 1,
    "medium": 2,
    "hard": 4,
}


@dataclass
class QuizQuestion:
    question: str
    correct_answer: str
    incorrect_answers: str


@dataclass
class QuizTaken:
    uuid: str
    difficulty: str
    questions: List[QuizQuestion]


@dataclass
class QuizResult:
    user_id: int
    quiz_uuid: str
    points: int


quizzes_taken: Dict[str, QuizTaken] = {}
quiz_results: Dict[str, List[QuizResult]] = defaultdict(list)


def calculate_points(quiz_taken: QuizTaken, answers: Dict) -> int:
    if len(quiz_taken.questions) != len(answers):
        raise ValueError("Inconsistent questions and answers.")

    points = 0
    for question, answer in zip(quiz_taken.questions, answers.values()):
        if answer == question.correct_answer:
            points += POINTS_MULTIPLIER[quiz_taken.difficulty]
    return points


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")
    first_name = db.Column(db.String(100), nullable=False, server_default="")
    last_name = db.Column(db.String(100), nullable=False, server_default="")

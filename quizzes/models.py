from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict

from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin

db = SQLAlchemy()


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


@dataclass
class FakeDatabase:
    quizzes_taken: Dict[str, QuizTaken] = field(default_factory=dict)
    quiz_results: Dict[str, List[QuizResult]] = field(default_factory=lambda: defaultdict(list))


fake_db = FakeDatabase()


POINTS_MULTIPLIER = {
    "easy": 1,
    "medium": 2,
    "hard": 4,
}


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

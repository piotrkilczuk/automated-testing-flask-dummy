from dataclasses import dataclass
from typing import List, Dict

from flask_user import UserMixin

from quizzes.app import db


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
quiz_results: Dict[str, List[QuizResult]] = []


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")
    first_name = db.Column(db.String(100), nullable=False, server_default="")
    last_name = db.Column(db.String(100), nullable=False, server_default="")


# class Quiz(db.Model):
#     __tablename__ = "quizzes"
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
#     difficulty = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
#
#
# class QuizQuestion(db.Model):
#     __tablename__ = "quiz_questions"
#     id = db.Column(db.Integer(), primary_key=True)
#     quiz_id = db.Column(db.Integer(), db.ForeignKey("quizzes.id", ondelete="CASCADE"))
#     question = db.Column(db.String(255), nullable=False)
#     correct_answer = db.Column(db.String(255), nullable=False)
#     incorrect_answer_1 = db.Column(db.String(255), nullable=False)
#     incorrect_answer_2 = db.Column(db.String(255), nullable=True)
#     incorrect_answer_3 = db.Column(db.String(255), nullable=True)
#
#
# class QuizResult(db.Model):
#     __tablename__ = "quiz_results"
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
#     difficulty = db.Column(db.String(255), nullable=False)
#     created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
#     points = db.Column(db.Integer(), nullable=False)

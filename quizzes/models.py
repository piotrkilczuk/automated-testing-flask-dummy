import enum
from typing import Dict

import flask_sqlalchemy
import flask_user

db = flask_sqlalchemy.SQLAlchemy()


class QuizDifficulty(enum.Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


POINTS_MULTIPLIER = {
    QuizDifficulty.EASY: 1,
    QuizDifficulty.MEDIUM: 2,
    QuizDifficulty.HARD: 4,
}


class User(db.Model, flask_user.UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    active = db.Column("is_active", db.Boolean(), nullable=False, server_default="1")
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")
    first_name = db.Column(db.String(100), nullable=False, server_default="")
    last_name = db.Column(db.String(100), nullable=False, server_default="")
    quiz_results = db.relationship("QuizResult", back_populates="user")


class QuizResult(db.Model):
    __tablename__ = "quiz_results"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="quiz_results")
    quiz_id = db.Column(db.Integer(), db.ForeignKey("quiz.id"))
    quiz = db.relationship("Quiz", back_populates="quiz_result")
    points = db.Column(db.Integer())


class QuizQuestion(db.Model):
    __tablename__ = "quiz_question"
    id = db.Column(db.Integer(), primary_key=True)
    quiz_id = db.Column(db.Integer(), db.ForeignKey("quiz.id"))
    quiz = db.relationship("Quiz", back_populates="quiz_questions")
    question = db.Column(db.String())
    correct_answer = db.Column(db.String())
    incorrect_answers = db.Column(db.JSON())


class Quiz(db.Model):
    __tablename = "quiz"
    id = db.Column(db.Integer(), primary_key=True)
    difficulty = db.Column(db.Enum(QuizDifficulty))
    quiz_result = db.relationship("QuizResult", back_populates="quiz")
    quiz_questions = db.relationship("QuizQuestion", back_populates="quiz")


def calculate_points(quiz: Quiz, answers: Dict) -> int:
    if len(quiz.quiz_questions) != len(answers):
        raise ValueError("Inconsistent questions and answers.")

    quiz.quiz_questions.sort(key=lambda q: q.id)

    points = 0
    for question, answer in zip(quiz.quiz_questions, answers.values()):
        if answer == question.correct_answer:
            points += POINTS_MULTIPLIER[quiz.difficulty]
    return points

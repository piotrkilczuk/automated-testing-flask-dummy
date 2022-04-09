from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager


class AppConfig:
    SECRET_KEY = "replace-me"

    SQLALCHEMY_DATABASE_URI = "sqlite://"  # In Memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_APP_NAME = "Quizzes"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True


app = Flask(__name__)
app.config.from_object(AppConfig())

db = SQLAlchemy(app)
quizzes = __import__("quizzes.models")
db.create_all()
user_manager = UserManager(app, db, quizzes.models.User)

__import__("quizzes.views")

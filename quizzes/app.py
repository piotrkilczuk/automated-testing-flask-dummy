from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager


class AppConfig:
    SECRET_KEY = "replace-me"

    SQLALCHEMY_DATABASE_URI = "sqlite://"  # In Memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_APP_NAME = "Quizzes"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True


def global_vars_report(response: Response) -> Response:
    print(f"{quizzes_taken=}")
    return response


app = Flask(__name__)
app.config.from_object(AppConfig())

db = SQLAlchemy(app)
quizzes = __import__("quizzes.models")
db.create_all()
User = quizzes.models.User
quizzes_taken = quizzes.models.quizzes_taken
user_manager = UserManager(app, db, User)
db.session.add(User(active=True, username="test", password=user_manager.hash_password("test")))
db.session.commit()

app.after_request(global_vars_report)


__import__("quizzes.views")

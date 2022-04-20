from flask import Flask, Response
from flask_user import UserManager


class AppConfig:
    SECRET_KEY = "replace-me"

    SQLALCHEMY_DATABASE_URI = "sqlite://"  # In Memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_APP_NAME = "Quizzes"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True


def init_database():
    from quizzes import models

    models.db.init_app(app)
    models.db.create_all()

    # Makes this function idempotent
    if not hasattr(app, "user_manager"):
        UserManager(app, models.db, models.User)

    models.db.session.add(models.User(active=True, username="test", password=app.user_manager.hash_password("test")))
    models.db.session.commit()


def global_vars_report(response: Response) -> Response:
    from quizzes import models

    print(f"{models.quizzes_taken=}")
    print(f"{models.quiz_results=}")
    return response


app = Flask(__name__)
app.config.from_object(AppConfig())
app.before_first_request(init_database)
app.after_request(global_vars_report)

__import__("quizzes.views")

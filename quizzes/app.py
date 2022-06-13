import flask
import flask_user


class AppConfig:
    SECRET_KEY = "replace-me"

    SQLALCHEMY_DATABASE_URI = "sqlite:///quizzes.db"  # In Memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_APP_NAME = "Quizzes"
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True


def bind_models(app: flask.Flask):
    from quizzes import models

    models.db.init_app(app)

    flask_user.UserManager(app, models.db, models.User)


def prepare_database():
    from quizzes import models

    models.db.create_all()


def bind_views(app: flask.Flask):
    from quizzes import views

    app.register_blueprint(views.blueprint)


def create_app():
    app = flask.Flask(__name__)
    app.config.from_object(AppConfig())
    bind_models(app)
    bind_views(app)
    app.before_first_request(prepare_database)
    return app

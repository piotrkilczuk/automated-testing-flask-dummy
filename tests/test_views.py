import pytest
from flask_login import FlaskLoginClient

from quizzes.app import create_app, prepare_database
from quizzes.models import User, db


@pytest.fixture
def flask_app():
    app = create_app()
    app.config.update({"SQLALCHEMY_DATABASE_URI": "sqlite://"})  # In memory
    with app.app_context():
        prepare_database()
        yield app


@pytest.fixture
def unauthenticated_client(flask_app):
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def authenticated_client(flask_app):
    user = User(active=True, username="test", password=flask_app.user_manager.hash_password("test"))
    db.session.add(user)
    db.session.commit()

    flask_app.test_client_class = FlaskLoginClient
    with flask_app.test_client(user=user) as client:
        yield client


def test_choose_quiz_difficulty_unauthenticated(unauthenticated_client):
    response = unauthenticated_client.get("/quiz")
    assert response.status_code == 302, response.text


def test_choose_quiz_difficulty_authenticated(authenticated_client):
    response = authenticated_client.get("/quiz")
    assert response.status_code == 200, response.text

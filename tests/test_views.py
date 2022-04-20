import pytest
from flask_login import FlaskLoginClient
from flask_user import UserManager

from quizzes.app import app, init_database
from quizzes.models import User, db


@pytest.fixture
def unauthenticated_client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def authenticated_client(prepare_database):
    user = User.query.one()
    app.test_client_class = FlaskLoginClient
    with app.test_client(user=user) as client:
        yield client


@pytest.fixture
def prepare_database():
    with app.app_context():
        init_database()
        yield


def test_choose_quiz_difficulty_unauthenticated(unauthenticated_client):
    response = unauthenticated_client.get("/quiz")
    assert response.status_code == 302, response.text


def test_choose_quiz_difficulty_authenticated(authenticated_client):
    response = authenticated_client.get("/quiz")
    assert response.status_code == 200, response.text

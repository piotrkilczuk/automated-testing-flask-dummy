from uuid import uuid4

from quizzes.models import calculate_points, QuizTaken


def test_calculate_points_dummy():
    quiz_taken = QuizTaken(uuid=uuid4().hex, difficulty='easy', questions=[])
    assert 0 == calculate_points(quiz_taken=quiz_taken, answers={})


from quizzes import models


def test_calculate_points_dummy():
    quiz = models.Quiz(difficulty=models.QuizDifficulty.EASY)
    assert 0 == models.calculate_points(quiz=quiz, answers={})

automated-testing-flask-dummy
=============================

Provides basic functionality of a Quizzes App for the Automated Testing Course.

Clone this and adjust to your liking and testing requirements.

Installation
------------

Either install this using the provided Poetry lockfile, or, if not using Poetry, use the `requirements.txt` provided.

Running
-------

```shell
FLASK_APP=quizzes.app flask run
```

Persistence
-----------

Uses SQLite for Users, global variable `quizzes/models.py:38` for Quiz data. Adjust to your needs.

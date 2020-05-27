import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # TODO: test for categories
    # TODO: test for retrieving questions
    # TODO: failure test for retrieving questions (invalid page number)
    # TODO: test for deleting question
    # TODO: failure test for deleting question (ID does not exist)
    # TODO: failure test for deleting question (500 error?)
    # TODO: test for creating question
    # TODO: test for searching for question, known to match
    # TODO: test for searching for question, known to not exist
    # TODO: failure test, bad data on search/create endpoint
    # TODO: failure test, creating question failure
    # TODO: test for getting questions by category
    # TODO: failure test, attempt to get questions for invalid category
    # TODO: failure test, attempt to get page of questions beyond allowance
    # TODO: test for quiz - all categories
    # TODO: test for quiz - filtered by category
    # TODO: test for 400 error
    # TODO: test for 404 error
    # TODO: test for 410 error
    # TODO: test for 422 error
    # TODO: test for 500 error


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

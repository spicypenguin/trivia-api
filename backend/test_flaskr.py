import os
import unittest
import json
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{db_usr}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(
            db_usr=os.getenv('DB_USER'),
            db_pwd=os.getenv('DB_PWD'),
            db_host=os.getenv('DB_HOST'),
            db_port=os.getenv('DB_PORT'),
            db_name=self.database_name
        )
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

    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['categories'], dict)

    def test_post_categories(self):
        res = self.client().post('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'], 'method not allowed')
        self.assertTrue(data['error'], 405)

    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertIsNone(data['current_category'])
        self.assertIsInstance(data['categories'], dict)
        self.assertIsInstance(data['total_questions'], int)
        self.assertLessEqual(len(data['questions']), 10)

    def test_get_questions_valid_page(self):
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertIsNone(data['current_category'])
        self.assertIsInstance(data['categories'], dict)
        self.assertIsInstance(data['total_questions'], int)
        self.assertLessEqual(len(data['questions']), 10)

    def test_get_questions_valid_page(self):
        res = self.client().get('/api/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertTrue(data['error'], 404)

    def test_delete_existing_question(self):
        res = self.client().delete('/api/questions/10')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 'OK')

    def test_delete_invalid_question(self):
        res = self.client().delete('/api/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 410)
        self.assertFalse(data['success'])
        self.assertTrue(data['message'], 'resource gone')
        self.assertTrue(data['error'], 410)

    def test_create_new_question(self):
        body = {
            'question': 'Why did the dog cross the road?',
            'answer': 'To get to the other side',
            'category': 5,
            'difficulty': 1
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/questions', data=json.dumps(body), headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_create_new_question_missing_data(self):
        body = {
            'question': 'Why did the dog cross the road?',
            'category': 5,
            'difficulty': 1
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/questions', data=json.dumps(body), headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_search_for_questions(self):
        body = {
            'searchTerm': 'a'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/questions', data=json.dumps(body), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['total_questions'], int)
        self.assertIsNone(data['current_category'])
        self.assertEqual(len(data['questions']), data['total_questions'])
        self.assertGreater(len(data['questions']), 0)

    def test_search_for_questions_case_sensitive(self):
        search_term = 'What'
        body_lower = {
            'searchTerm': search_term.lower()
        }
        body_upper = {
            'searchTerm': search_term.upper()
        }

        headers = {
            'Content-Type': 'application/json'
        }
        res_lower = self.client().post(
            '/api/questions', data=json.dumps(body_lower), headers=headers)
        res_upper = self.client().post(
            '/api/questions', data=json.dumps(body_upper), headers=headers)

        data_lower = json.loads(res_lower.data)
        data_upper = json.loads(res_upper.data)

        self.assertEqual(res_lower.status_code, 200)
        self.assertEqual(res_upper.status_code, 200)
        self.assertListEqual(data_lower['questions'], data_upper['questions'])

    def test_search_for_unmatching_string(self):
        body = {
            'searchTerm': 'nonsensicalstringthatwillnotMatchanything'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/questions', data=json.dumps(body), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertIsInstance(data['total_questions'], int)
        self.assertIsNone(data['current_category'])
        self.assertEqual(len(data['questions']), data['total_questions'])
        self.assertEqual(len(data['questions']), 0)

    def test_create_or_search_bad_request(self):
        body = {
            'invalid_payload': True
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/questions', data=json.dumps(body), headers=headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')
        self.assertTrue(data['error'], 400)

    def test_get_questions_by_category(self):
        res = self.client().get('/api/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['questions'], list)
        self.assertIsNotNone(data['current_category'])
        self.assertIsInstance(data['total_questions'], int)
        self.assertTrue(len(data['questions']) <= 10)

    def test_get_questions_by_category_invalid_page(self):
        res = self.client().get('/api/categories/1/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertTrue(data['error'], 404)

    def test_get_questions_by_category_invalid_category(self):
        res = self.client().get('/api/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertTrue(data['error'], 404)

    def test_run_quiz_no_category(self):
        body = {
            'quiz_category': {'type': 'click', 'id': 0},
            'previous_questions': []
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/quizzes', data=json.dumps(body), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['question'], dict)

    def test_run_quiz_category_selected(self):
        category_id = 1
        body = {
            'quiz_category': {'type': 'Science', 'id': category_id},
            'previous_questions': []
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/quizzes', data=json.dumps(body), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['question'], dict)
        self.assertEqual(data['question']['category'], category_id)

    def test_run_quiz_category_selected_no_questions_remain(self):
        category_id = 1
        body = {
            'quiz_category': {'type': 'Science', 'id': category_id},
            'previous_questions': [20, 21, 22]
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/quizzes', data=json.dumps(body), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNone(data['question'])

    def test_run_quiz_invalid_category(self):
        body = {
            'quiz_category': {'type': 'Unknown', 'id': 100},
            'previous_questions': []
        }
        headers = {
            'Content-Type': 'application/json'
        }
        res = self.client().post('/api/quizzes', data=json.dumps(body), headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertTrue(data['error'], 404)

    # TODO: test for 422 error
    # TODO: test for 500 error


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Helper functions


def get_start_and_end(page):
    return page - 1, page * QUESTIONS_PER_PAGE


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # allow cross-origin requests to /api/* from all origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """Append CORS headers to all responses."""
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    @app.route('/api/categories')
    def get_categories():
        """Return a dictionary of all categories."""
        # Get all categories
        categories = Category.query.all()

        return jsonify({
            'categories': {
                category.format()['id']: category.format()['type']
                for category in categories
            },
            'success': True
        })

    @app.route('/api/questions')
    def get_questions():
        """Return a dictionary containing paginated questions.

        Querystring parameter:
        page - which page of questions to retrieve (default 1); optional
        """
        # get the page, expected to be an integer, default to 1 if not found
        page = request.args.get('page', default=1, type=int)

        # get all questions, sorted by Question.id
        questions = Question.query.order_by(Question.id).all()

        # get all categories
        categories = Category.query.all()

        # calculate the start and end page numbers
        start, end = get_start_and_end(page)

        return jsonify({
            'questions': [question.format() for question in questions][start:end],
            'current_category': None,
            'categories': {
                category.format()['id']: category.format()['type']
                for category in categories
            },
            'total_questions': len(questions),
            'success': True
        })

    @app.route('/api/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """Delete a question with a given question id.

        URL parameter:
        question_id - which question to delete; mandatory
        """
        error = 0
        try:
            # try and retrieve the question matching the given ID
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question:
                # if question found, delete it
                question.delete()
            else:
                # if question not found, raise a 410 error
                error = 410
        except:
            # if retrieval or deletion failed, raise a 500 error
            error = 500

        if error > 0:
            # raise an error with the appropriate code if any failure occured
            abort(error)
        else:
            # otherwise return a success JSON payload
            return jsonify({
                'status': 'OK',
                'success': True
            })

    @app.route('/api/questions', methods=['POST'])
    def create_question():
        """Create new question, or search for question."""
        data = request.get_json()

        # if `searchTerm` present, execute a search
        if data.get('searchTerm'):
            return search_for_questions(data)

        # else if `question` present, create new question
        elif data.get('question'):
            return create_new_question(data)

        # otherwise there is a data issue, fail out
        else:
            abort(400)

    def create_new_question(data):
        """Create a new question.

        Takes question, answer, category, difficulty entered from UI.
        Creates new question object and persists to db.
        """
        try:
            question = Question(
                question=data.get('question'),
                answer=data.get('answer'),
                category=data.get('category'),
                difficulty=data.get('difficulty')
            )
            question.insert()
            return jsonify({
                'success': True
            })
        except:
            # raise a 500 error if insert to db failed
            abort(500)

    def search_for_questions(data):
        """Search for questions using case-insensitive matching on question.

        Body parameters
        searchTerm - the keyword to match against the questions in the db
        """
        search_term = data.get('searchTerm')

        # filter questions using as case-insensitive match against Question.question
        matches = Question.query.filter(Question.question.ilike(
            f'%{search_term}%')).order_by(Question.id).all()

        # QUESTION: do search results also need to be paginated?
        return jsonify({
            'questions': [question.format() for question in matches],
            'total_questions': len(matches),
            'current_category': None,
            'success': True
        })

    @app.route('/api/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        """Return paginated list of questions for a given category."""
        # get all questions matching a category ID
        questions = Question.query.filter(
            Question.category == category_id).order_by(Question.id).all()

        # get the name of the category being requested
        category = Category.query.filter(
            Category.id == category_id).one_or_none()

        # determine start/end for pagination
        page = request.args.get('page', default=1, type=int)
        start, end = get_start_and_end(page)

        if category or start > len(questions):
            return jsonify({
                'questions': [q.format() for q in questions][start:end],
                'current_category': category.type,
                'total_questions': len(questions),
                'success': True
            })
        else:
            # category requested could not be found, or page is invalid
            abort(404)

    @app.route('/api/quizzes', methods=['POST'])
    def run_quiz():
        """Generate next question for the quiz."""
        data = request.get_json()

        # retrieve the category that the user is requesting data for
        category = int(data.get('quiz_category').get('id', 0))
        print(category)

        # retrieve the questions the user has already completed
        previous_questions = data.get('previous_questions', [])

        # if "ALL" selected, category ID is 0
        if category > 0:
            # get all questions (not yet asked) for the specified category
            questions = Question.query.filter(
                Question.category == category,
                ~Question.id.in_(previous_questions)
            ).all()
        else:
            # get all questions (not yet asked) for all categories
            questions = Question.query.filter(
                ~Question.id.in_(previous_questions)
            ).all()

        # randomly shuffle questions
        random.shuffle(questions)

        # if questions was empty (no questions remain), question will be None
        question = None

        if len(questions) > 0:
            # if questions remain, set question to the first in list
            question = questions[0].format()

        return jsonify({
            'success': True,
            'question': question
        })

    #########
    # Custom error handlers
    #########

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 400,
            'success': False,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'error': 404,
            'success': False,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(410)
    def resource_gone(error):
        return jsonify({
            'error': 410,
            'success': False,
            'message': 'resource gone'
        }), 410

    @app.errorhandler(422)
    def unprocessable_request(error):
        return jsonify({
            'error': 422,
            'success': False,
            'message': 'unprocessable request'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'error': 500,
            'success': False,
            'message': 'internal server error'
        }), 500

    return app

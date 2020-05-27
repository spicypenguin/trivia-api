# Full Stack Trivia API Backend

## Getting Started

### Automated setup

If you have the following dependencies installed and running, you can leverage the provided setup scripts to get started more quickly:

- `python 3.7+`
- `pyenv`
- `postgresql`

To use the setup script, run `bin/setup.sh`.

### Manual setup

If you are unable to use `bin/setup.sh` you can follow the steps below to get started.

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
postgres createuser caryn
postgres createdb trivia
psql trivia < trivia.psql
```

## Setting environment variables

The application requires the following environment variables to be set to establish connectivity with the db:

* `DB_USER`
* `DB_PWD`
* `DB_HOST`
* `DB_PORT`
* `DB_NAME`

Alternatively, you can setup a file named `.env` that has these variables included in it, which will be automatically set as environment variables when the application is started. 

Structure of the `.env` file:

```
DB_USER=
DB_PWD=
DB_HOST=
DB_PORT=
DB_NAME=
```

## Running the server

Once you have all dependencies setup, you have initialsed the database, and set your environment variables, you are now ready to run the backend of the application.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --port 1234
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## API Documentation

#### GET `/api/categories`
- Fetches a list of all caegories
- Request Arguments: None
- Response: An object with two keys, categories and success, where success is always `True`, and categories is an object of key:value pairs (Category.id:Category.type)
    ```
    {
        'categories': {
            '1': 'Science',
            '2': 'Art',
            '3': 'Geography',
            '4': 'History',
            '5': 'Entertainment',
            '6': 'Sports'
        },
        'success': True
    }
    ```

#### GET `/api/questions`
- Fetches a list of all questions, paginated into pages of `10` questions
- List is ordered by `Question.id` for consistent diplay
- Request Arguments: 
    - `page` (integer, optional, defaults to `1`)
- Response:
    ```
    {
        'questions': [
            {
                'id': 5
                'question': '',
                'answer': '',
                'category': 1,
                'difficulty': 5 
            },
            {...}
        ],
        'current_category': None,
        'categories': {
            '1': 'Science',
            '2': 'Art',
            '3': 'Geography',
            '4': 'History',
            '5': 'Entertainment',
            '6': 'Sports'
        },
        'total_questions': 19
        'success': True
    }
    ```

#### POST `/api/questions`
- Create a new question, or search for existing questions
- Request Arguments: None
- Request Body:
    - For create: An object with 4 keys: `question`, `answer`, `category`, and `difficulty`
        ```
        {
            'question': '',
            'answer': '',
            'category': '',
            'difficulty': ''
        }
        ```
    - For search: An object with 1 key - `searchTerm` - indicating the word being searched for
        ```
        {
            'searchTerm': ''
        }
        ```
- Response:
    - For create:
        ```
        {
            'success': True,
            'question': {
                'id': '',
                'question': '',
                'answer': '',
                'category': '',
                'difficulty': ''
            }
        }
        ```
    - For search
        ```
        {
            'questions': [ 
                {
                    'id': 5
                    'question': '',
                    'answer': '',
                    'category': 1,
                    'difficulty': 5 
                },
                {...}
            ],
            'total_questions': 5,
            'current_category': None,
            'success': True
        }
        ```
- Raises: The following errors can occur when calling this endpoint
    - `400`: The body provided in the initial `POST` did not match the requirements for either search or create
    - `422`: An error happened when attempting to create the new question

#### DELETE `/api/questions/<question_id>`
- Removes a question from the database, based on the provided ID
- Request Arguments:
    - `question_id` (integer, mandatory)
- Response:
    ```
    {
        'status': 'OK',
        'success': True
    }
    ```
- Raises: The following errors can occur when calling this endpoint
    - `410`: Question that you requested to delete was not found
    - `500`: An error happened when attempting to retrieve and delete the question



#### GET `/api/categories/<category_id>/questions`
- Fetches a list of all questions within a given category, paginated into groups of 10 questions at a time
- List is ordered by `Question.id` for consistent diplay
- Request Arguments: 
    - `category_id` (integer, mandatory)
    - `page` (integer, optional, defaults to `1`)
- Response:
    ```
    {
        'questions': [],
        'current_category': None,
        'total_questions': 19
        'success': True
    }
    ```
- Raises: The following errors can occur when calling this endpoint
    - `404`: Invalid category ID provided
    - `404`: Invalid page number provided (out of range of questions)

#### POST `/api/quizzes`
- Initiates (or continues) a quiz, returning a question at random from the selected category (or any category, if "ALL" was selected by the user as the desired category)
- Once all questions are exhausted, question will be returned as `None` (`null`)
- Request Arguments: None
- Request Body: Object containing two keys, `quiz_category` and `previous_questions`
    - `quiz_category`: An object describing the users selected category (optional)
    - `previous_questions` A list of previous question IDs the user has completed in this quiz
    ```
    {
        quiz_category: {
            'type': 'Science',
            'id': '1'
        },
        previous_questions: [1, 2, 3]
    }
    ```
- Response: An object with two keys, `success` and `question`, where `question` is an object containing details of the next question to ask. Question can be None, which indicates there are no more questions left and the quiz is over.
    ```
    {
        success: True,
        question: {
            'id': 5
            'question': '',
            'answer': '',
            'category': 1,
            'difficulty': 5 
        }
    }
    ```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

Alternatively, you can run all of the commands above by executing:

`bin/test.sh`

## Future feature requests

Development on a full stack web application is never done. Here are some things at the top of our wish list for future iterations:

* [] Switch database setup from `trivia.psql` to use `Flask-migrate` enabling more effective schema migrations
* [] Make __init__.py more modular, breaking out classes into their own hierarchy
* [] Implement `swagger` for API documentation to make API docs more connected with the API that is developed
* [] Refactor `/api/questions` and `/api/categories/<id>/questions` into a single helper function

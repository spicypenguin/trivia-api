# Udacitriva - Full Stack API Final Project

## Full Stack Trivia

Udacity is creating a trivia web application, to assist participants in their online education programs to bond about things other than the work that they are doing. Udacitrivia is a user-led trivia application, where users can view existing trivia questions, view questions by category, and submit their own questions to the system. They can also run mini trivia quizzes to put their knowledge to the test, drawing from the corpus of questions that are available in the system.

The frontend of the application is built in `React.js`, and the app is backed by a `python` backend which exposes APIs via `Flask`. Data for the application is modelled and stored in a `postgres` database.

## About the app

The app is fully functional, and comes complete with unit tests that cover all core APIs that power the application. It also has some useful helper scripts to get you up and started quickly with any local development effort.

### Backend

The `./backend` directory contains the Flask and SQLAlchemy server. Refer to the [README.md](./backend/README.md) under that directory for information on getting started with the backend.

Quick start: `cd ./backend && bin/setup.sh && export FLASK_APP=flaskr && export FLASK_ENV=development && flask run --port 1234`

### Frontend

The `./frontend` directory contains the React frontend to consume the data from the Flask server.  Refer to the [README.md](./frontend/README.md) under that directory for information on getting started with the frontend.

Quick start: `npm install && npm start`

## Authors

Jeff Sinclair (Spicypenguin)

## Acknowledgements

The course content provided during the [Udacity full stack web development nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).
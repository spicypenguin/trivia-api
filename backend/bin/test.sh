sudo -u postgres dropdb trivia_test
sudo -u postgres createdb trivia_test
sudo -u postgres psql trivia_test < trivia.psql
python test_flaskr.py
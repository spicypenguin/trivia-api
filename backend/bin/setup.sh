pyenv virtualenv trivia-api
source activate trivia-api
pip install -r requirements.txt
sudo -u postgres createuser caryn
sudo -u postgres psql < trivia.psql
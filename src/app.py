import os
from src.config import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

source_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_dir = os.path.join(source_dir, 'templates')
static_dir = os.path.join(source_dir, 'static')


app = Flask(__name__, template_folder=templates_dir, static_folder=static_dir)
yml_dir = os.path.abspath(os.path.join(os.curdir, 'config.yml'))
app.config.from_yaml(yml_dir)
app.config.from_yaml(yml_dir, field='DATABASE')
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)


from views_game import *
from views_user import *

if __name__ == '__main__':
    app.run()

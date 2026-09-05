import os
from dotenv import load_dotenv
from pathlib import Path

from flask import Flask, request, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_babel import Babel


env_path = Path(__file__).resolve().parent.parent / 'EcoS.env'
load_dotenv(dotenv_path=env_path)

# Flask Babel config
def get_locale():
    if 'lang' in request.args:
        lang = request.args.get('lang')
        if lang in ['en', 'fr', 'ar']:
            session['lang'] = lang
            return session['lang']
    elif 'lang' in session:
        return session.get('lang')
    return request.accept_languages.best_match(['en', 'fr', 'ar'])

def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

app = Flask(__name__)

# Use secret key from .env
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database configuration (PostgreSQL)
host = os.getenv('DB_HOST')
port_str = int(os.getenv('DB_PORT'))
print("Loaded port:", port_str)  # Add this for debugging
port = int(port_str)
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# Configuring Babel
babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'

# Use mail password from .env
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_ADRESSE'] = os.getenv('MAIL_ADRESSE')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

from EcoS import routes
import os
from models import OAuth
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import (OAuthConsumerMixin, SQLAlchemyStorage)
from flask_login import (LoginManager, UserMixin, current_user, login_user, logout_user)

path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(path, 'app.db')




class Config(object):
    
    SECRET_KEY= 'mamarrone'
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'fa3864818@gmail.com'
    MAIL_PASSWORD = 'fkraatstyfrstyny'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
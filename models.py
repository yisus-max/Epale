from logging import error
from unicodedata import name
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.storage.sqla import (OAuthConsumerMixin, SQLAlchemyStorage)
from flask_login import (LoginManager, UserMixin, current_user, login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime
from itsdangerous import URLSafeTimedSerializer
from flask_migrate import Migrate





login_manager = LoginManager()



db = SQLAlchemy()





class User(db.Model, UserMixin):
  __tablename__ = 'users'
  
  id = db.Column(db.Integer, primary_key =True)
  image_file = db.Column(db.String(250), nullable = False, default = 'user.png')
  name = db.Column(db.String(256))
  username = db.Column(db.String(100))
  password = db.Column(db.String(300))
  email = db.Column(db.String(1000), unique = True)
  create_date = db.Column(db.DateTime, default = datetime.datetime.now)
  posts = db.relationship('Post', backref = 'blog')
  
  




  def get_token(self):
    serial = URLSafeTimedSerializer('Thisisasecret')
    return serial.dumps({'user_id': self.id})

  @staticmethod
  def verify_token(token):
    serial = URLSafeTimedSerializer('Thisisasecret')
    try:
     user_id = serial.loads(token, max_age= 300)['user_id']
    except:
      return None
      
    return User.query.get(user_id)


 
  def __init__(self, username,  password, email, name):
     self.username = username
     self.password = self.__create_password(password)
     self.email = email
     self.name = name

    
  def __create_password(self, password):
     return generate_password_hash(password)

  def verify_password(self, password):
     return check_password_hash(self.password, password)


class OAuth(OAuthConsumerMixin, db.Model):

   
  provider_user_id = db.Column(db.String(256), unique = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  user = db.relationship(User)
 

class Comment(db.Model, UserMixin):

  
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(256), unique = True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  name = db.Column(db.String(256))
  text = db.Column(db.Text())
  create_date = db.Column(db.DateTime, default = datetime.datetime.now)

class Post(db.Model, UserMixin):
    __tablename__ = 'poster'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(256)) 
    content = db.Column(db.Text()) 
    author = db.Column(db.String(256) )
    slug = db.Column(db.String(256)) 
    create_date = db.Column(db.DateTime, default = datetime.datetime.now)
    vin_id = db.Column(db.Integer, db.ForeignKey('users.id'))


  



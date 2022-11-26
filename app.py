import secrets
from random import choice, random, randint
from flask_login import login_required
from flask_dance.consumer.storage.sqla import (OAuthConsumerMixin, SQLAlchemyStorage)
from flask_dance.consumer import oauth_authorized
import os
import pathlib
from formsx import UpdateProfile, ResetPass,Forgot,login,commentx,formx, Postx, Searched
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests 
from flask import *
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash 
from config import DevelopmentConfig
from models import db
from models import User, Post
from flask import make_response
from flask_wtf import CSRFProtect
from flask.globals import session
from models import Comment
from flask_mail import *
from flask_mail import Message
import threading
from flask import copy_current_request_context
from itsdangerous import URLSafeTimedSerializer
from random import *
from models import OAuth, login_manager
import models
from flask_login import (LoginManager, UserMixin, current_user, login_user, logout_user)
from flask_dance.contrib.google import make_google_blueprint, google
from flask_migrate import Migrate
from flask_ckeditor import CKEditor



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
 

path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(path, 'app.db')




app =Flask(__name__, template_folder='static')
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
mail = Mail()
s = URLSafeTimedSerializer('Thisisasecret!')
login_manager = LoginManager()
login_manager.login_view = 'google.login'
migrate = Migrate()
ckeditor = CKEditor()







GOOGLE_CLIENT_ID = "622955328798-77kk3466cluueh8a77pu386nhvobseau.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
client_secret_file = os.path.join(pathlib.Path(__file__).parent, "client_j.json")



#RANDOM_USERNAME

aleatorio = ['asfasfgdshdfh', 'kguykuykvcngxfgse', 'kkdsghuwbggsdolgsodl', 'dhdjdjdgj', 'gasrgvsawe', 'hrthtrhds', 'adfhdfh', 'asfgaga', 'shshfdasfa', 'sghsdgs', 'fdhdfhdfhdf', 'jyjryjdh']

random_prof = choice(aleatorio)

adjetivos = ['pdjjdyfuyf', 'yrhekdkx', 'vyeneoxoa', 'oryvynsoewr', 'uthryixka']

random_adj = choice(adjetivos)

edad = randint(27, 1000)
edadx = randint(100000000000, 80000000000000000)


useraleatorio = random_prof + ' ' + random_adj + ' ' + str(edad)






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    



google_blueprint = make_google_blueprint(
    client_id= GOOGLE_CLIENT_ID,
    client_secret= GOOGLE_CLIENT_SECRET,
    scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
    offline=True,
    reprompt_consent=True,
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user))

app.register_blueprint(google_blueprint)




def send_email(user_email , username):

  

  email = user_email

  token  = s.dumps(email, salt = 'confirm-email')

  msg = Message('Email de confirmación en el registro', sender = app.config['MAIL_USERNAME']    , recipients= [user_email] )    

  link =  url_for('confirm_email', token = token , _external = True)

  msg.html = render_template('email.html' , user = username, link = link)

  mail.send(msg)

  return token

  
@app.errorhandler(404)
def page_error(e):
  return render_template('404.html'),404
@app.errorhandler(501)
def error_sql(error):
  return redirect('comment/google')

@app.context_processor
def bar():
  form = Searched()
  
  return dict(form = form)
   


@app.route('/search' , methods = ['POST'])
def search():

  form = Searched()
  post = Post.query


  if form.validate_on_submit():

    post_searched = form.searched.data
    post = post.filter(Post.content.like('%' + post_searched + '%' ))
    post = post.order_by(Post.title).all()
 
    return render_template('search.html', form = form, searched = post_searched, post = post)

@app.route('/admin_page/<int:id>/<username>', methods = ['GET', 'POST'])
@login_required 
def admin_page(id, username):


   
  post = User.query.get_or_404(id)
  postx = User.query.filter_by(id = id , username = username)
 
  form = UpdateProfile()
  
  if current_user.id  == 1 :              
 
   if request.method == "POST":
   
     if form.picture.data:
       
        picture_file = save_picture(form.picture.data)
        post.image_file = picture_file
        db.session.commit()
        return redirect(url_for('admin_page', id = current_user.id , username = current_user.username))
     
     try:
   
        post.username = request.form['username']
        post.email = request.form['email']
        post.image_file = request.files['picture']
        db.session.commit()
        flash('Cuenta actualizada!')
        return redirect(url_for('admin_page', id = current_user.id, username = current_user.username))

     except:

          db.session.rollback()  
          flash('Error al actualizar tu perfil, intenta nuevamente')   

   elif request.method == 'GET':

     form.username.data = current_user.username
     form.email.data = current_user.email

     image_file = url_for('static', filename = 'imagenes/' + post.image_file )

     return render_template('admin_page.html', form = form, image_file = image_file, post = post , postx = postx)   
      
  
  else:
    abort(404)



    
 
  

@app.route('/authorized')
def authorized():
  google_data = None
  user_info_endpoint = '/oauth2/v2/userinfo'
  if current_user.is_authenticated and google.authorized:
        google_data = google.get(user_info_endpoint).json()
  return render_template('index3.html',
                           google_data=google_data,
                           fetch_url= google.base_url + user_info_endpoint)
      




@oauth_authorized.connect_via(google_blueprint)
def google_logged_in(blueprint, token):
    resp = blueprint.session.get('/oauth2/v2/userinfo')
    user_info = resp.json()
    user_id = str(user_info['id'])
    oauth = OAuth.query.filter_by(provider=blueprint.name,
                                  provider_user_id=user_id).first()

  
         

    if not oauth:
        oauth = OAuth(provider=blueprint.name,
                      provider_user_id=user_id,
                      token= token)
    else:
        oauth.token = token
        db.session.add(oauth)
        db.session.commit()
        login_user(oauth.user)

        return redirect(url_for('account', id = current_user.id , username = current_user.username))

    if not oauth.user:

      try:

         user = User(email=user_info["email"],
                    name=user_info["name"], username = useraleatorio, password='default')
         oauth.user = user
         db.session.add_all([user, oauth])
         db.session.commit()
      

      except:

         db.session.rollback()
         flash('Ocurrio un error en el ingreso. Para iniciar sesión con Google debes haber iniciado por primera vez en ella. De lo contrario, inicia sesión con tu correspondiente "USERNAME" y contraseña.')
         return redirect(url_for('login_userx'))

        
        

    return False


@app.route('/protected')
@login_required
def protect():
  return "<h1> Hola protegido </h1>"

@app.route('/index')
@login_required
def index():

   return render_template('cookie.html')




@app.route('/logout')
def logout():

  logout_user()
  session.clear()

  return redirect(url_for('login_userx'))


@app.route('/login', methods= ['GET', 'POST']) 
def login_userx():

  if current_user.is_authenticated:
     return redirect(url_for("index"))


  form = login()

  if form.validate_on_submit():
    
    username = form.username.data
    password = form.password.data 
    
   
    

    user = User.query.filter_by(username = username).first()
    
    
   
    if user is not None and user.verify_password(password):
       login_user(user)
       
       
       success_message = 'Te haz logeado con exito!!: {}'.format(username)
       flash(success_message)
       
       
       return redirect(url_for('account', id = current_user.id , username = current_user.username))

      
      

    else:
      error_message = 'Usuario o contraseña no validos'
      flash(error_message)
      
     
    
  return render_template('login.html', form = form)




@app.route('/comment', methods = ['GET', 'POST'])
@login_required
def comentar():

  form = commentx()
       
    
  
  if form.validate_on_submit():
      
    
       new_note = Comment(text = form.comentario.data, user_id = current_user.id)
       db.session.add(new_note)
       db.session.commit()

       
   
       
  return render_template('comment.html', form = form)


@app.route('/reviews/<int:page>', methods = ['GET'])
def reviews(page = 1):
  per_page = 5

  comment_list = Comment.query.join(User).add_columns(User.name, Comment.text , Comment.create_date).paginate(page,per_page,False)



  return render_template('reviews.html',  comments = comment_list )   


def save_picture(form_picture):


  random_hex = secrets.token_hex(16)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext 
  picture_path = os.path.join(app.root_path, 'static/imagenes', picture_fn)
  form_picture.save(picture_path)


  return picture_fn




@app.route('/account/<int:id>/<username>', methods = ['GET', 'POST'])
@login_required
def account(id, username):
   
  post = User.query.get_or_404(id)
  postx = User.query.filter_by(id = id , username = username)
 
  form = UpdateProfile()
  
                 
 
  if request.method == "POST":
   
    if form.picture.data:
       
       picture_file = save_picture(form.picture.data)
       post.image_file = picture_file
       db.session.commit()
       return redirect(url_for('account', id = current_user.id , username = current_user.username))
     
    try:
   
       post.username = request.form['username']
       post.email = request.form['email']
       post.image_file = request.files['picture']
       db.session.commit()
       flash('Cuenta actualizada!')
       return redirect(url_for('account', id = current_user.id, username = current_user.username))

    except:

         db.session.rollback()  
         flash('Error al actualizar tu perfil, intenta nuevamente')   

  elif request.method == 'GET':

   form.username.data = current_user.username
   form.email.data = current_user.email

  image_file = url_for('static', filename = 'imagenes/' + post.image_file )
  



  return render_template('account.html', form = form, image_file = image_file, post = post , postx = postx)                                                
 
@app.route('/update_profile/<int:id>', methods = ['GET', 'POST'])
def update_profile(id):

  form = UpdateProfile()
  user = User.query.get_or_404(id)


  if request.method == "POST":

    user.username = request.form['username']
    user.email = request.form['email']

    try:  
       db.session.commit()
       flash('Datos de perfil actualizado!')
       return render_template('update_profile.html', form = form, user = user)

    except:
      db.session.rollback()  
      flash('Error al actualizar tu perfil, intenta nuevamente')
      return render_template('update_profile.html', form = form, user = user)

   
  form.username.data = user.username
  form.email.data = user.email
   

  return render_template('update_profile.html', form = form , user = user)


 

@app.route('/create' , methods=['GET' , 'POST'])
def create():

  
  form = formx()

  if current_user.is_authenticated:
     return redirect(url_for("index"))
  
  if form.validate_on_submit():

    global userx


    userx = User(  form.username.data,
                   form.password.data,
                   form.email.data,
                  form.name.data)
         
  
    @copy_current_request_context
    def send_message(email,username):
        send_email(email,username)
        confirm_email()

    sender = threading.Thread(name = 'mail sender' , target =  send_message ,   args = (userx.email, userx.username ))
    sender.start()



    success_message = 'Confirma tu correo electronico'
    flash(success_message)
   

  else:

    print ("Error en el formulario")
 
  return render_template('base2.html' , form = form) 
 
@app.route('/confirm_email/<token>' , methods = ['GET', 'POST'])

def confirm_email(token):
   
   

   try:
    email = s.loads(token, salt = 'confirm-email', max_age=300)
    db.session.add(userx)
    db.session.commit()

    success_message = 'Haz confirmado tu email! , ahora puedes logearte'
    flash(success_message)

   except Exception:
      success_message = 'Correo de confirmación expirado '
      flash(success_message)
      return redirect(url_for('create'))
 
   return redirect(url_for('login_userx'))


def send_emailp(user):

  token = User.get_token(user)

  msg = Message('Reinicio de contraseña requerida', sender = app.config['MAIL_USERNAME'] , recipients= [user.email])

  link =  url_for('reset', token = token , _external = True)

  msg.html = render_template('email_forgot.html' , link = link, user = user)

  mail.send(msg)


@app.route('/reset/<token>', methods = ['GET', 'POST']) 
def reset(token):



  user = User.verify_token(token)
  if user is None:
    error_message = 'Link expirado o invalido!, por favor intenta nuevamente'
    flash(error_message )
    return redirect(url_for('login_userx'))
  
  
  form = ResetPass()

  if form.validate_on_submit():

    password_crypt = models.generate_password_hash(form.password.data)
    user.password = password_crypt
    db.session.commit()
    success_message = 'Se ha cambiado tu contraseña correctamente'
    flash(success_message)
    return redirect(url_for('login_userx'))

  return render_template('reset.html', form = form )




@app.route('/forgot', methods = ['GET', 'POST'])
def forgot(): 
  form = Forgot()
  
  if form.validate_on_submit():

    user = User.query.filter_by(email = form.email.data).first()


    if user:
     send_emailp(user)

     flash('Correo de reinicio de contraseña enviado, revisa tu correo!')

     return redirect(url_for('login_userx'))


  return render_template('forgot.html', form = form)

@app.route('/published/<int:page>', methods = ['GET', 'POST'])
def published_posts(page = 1):
   
  per_page = 5
 

  post = Post.query.order_by(Post.create_date).paginate(page,per_page,False)


        
  return render_template('posts.html', post= post) 

@app.route('/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
def delete_post(id):
  post_delete = Post.query.get_or_404(id)


  if post_delete.blog.id != current_user.id or post_delete.blog.id != 1: 
    abort(403)

  db.session.delete(post_delete)
  db.session.commit()
  flash('Post eliminado!')

  return redirect(url_for('published_posts', page = 1))
  

  

@app.route('/post/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit_post(id):

  form = Postx()
  post = Post.query.get_or_404(id)


  if form.validate_on_submit():
    
    post.title = form.title.data
    post.author = form.author.data
    post.slug = form.slug.data
    post.content = form.content.data
    post.vin_id = post.vin_id

    db.session.add(post)
    db.session.commit()

    message = 'Blog actualizado con exito!'
    flash(message)

    return redirect(url_for('publish_post', id = post))



  if current_user.id == post.blog.id or current_user.id == 1:

   form.title.data = post.title
   form.author.data = post.author
   form.slug.data = post.slug
   form.content.data = post.content

   return render_template('editpost.html', form = form) 

  else: 
    flash('No puedes editar este post!')
    return redirect(url_for('published_posts', page= 1))
  

 
@app.route('/poster/<int:id>', methods = ['GET', 'POST'])
def poster(id):
  post = Post.query.get_or_404(id)
  





  return render_template('post.html', post = post)


    
 
  

@app.route('/publish-post', methods = ['GET', 'POST'])
@login_required
def publish_post():
  
 

  form = Postx()

  if form.validate_on_submit():

    blog = current_user.id
   
    post = Post(title = form.title.data , content = form.content.data , author = current_user.username , slug = form.slug.data,  vin_id = blog )
    
    form.title.data = ''
    form.content.data = ''
    form.author.data = ''
    form.slug.data = ''

    db.session.add(post)
    db.session.commit()

    message = 'Blog creado con exito!'
    flash(message)
  

  return render_template('publish_post.html', form = form )





csrf.init_app(app)
db.init_app(app)
mail.init_app(app)
migrate.init_app(app,db)
ckeditor.init_app(app)
login_manager.init_app(app)




with app.app_context():
  db.create_all()

if __name__ == "__main__":
  app.run()









#@app.route('/<lista>')
#def index(args, lista = [1,2,3,4,5]):
 #return render_template('indexx.html', my_list = lista)
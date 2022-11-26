from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask import flash
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields import EmailField
from wtforms.fields import PasswordField
from wtforms.validators import ValidationError
from wtforms import  validators
from wtforms import HiddenField
import wtforms_html5
from flask import request
from flask_sqlalchemy import SQLAlchemy
from models import User
from flask_login import current_user
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField



def honey_x(form, field):
    if len(field.data) > 0:
      raise validators.ValidationError('El campo debe estar vacio')

class formx(FlaskForm):


    name =  TextAreaField('FULL NAME',[validators.length(min=4,max=25, message='Ingresa un nombre y apellido valido' ),validators.DataRequired(message="El nombre es requerido")])
    username = TextAreaField('USERNAME',[validators.length(min=4,max=25, message='Ingresa un username valido' ),validators.DataRequired(message="El username es requerido")])
    email = EmailField('EMAIL',[validators.length(min=4,max=350, message= 'Introduzca un correo electronico valido'), validators.DataRequired(message= "El correo es requerido"), validators.Email(message = 'Por ravor ingrese un correo electronico valido')])
    password = PasswordField('PASSWORD',[validators.length(min=1,max=305, message='Ingresa una contraseña valida' ),validators.DataRequired(message="La contraseña es requerida")])
    

    def validate_username(form,field):
      username = field.data
      user = User.query.filter_by(username = username).first()
      if user is not None:
       raise validators.ValidationError('Usuario ya existente!')

    def validate_email(form,field):
      email = field.data
      mailx = User.query.filter_by(email = email).first()
      if mailx is not None:
       raise validators.ValidationError('Correo electronico ya registrado!')
      

class UpdateProfile(FlaskForm):

    username = TextAreaField('USERNAME',[validators.length(min=4,max=25, message='Ingresa un username valido' ),validators.DataRequired(message="El username es requerido")])
    email = EmailField('EMAIL')
    picture = FileField('Actualizar foto de perfil', validators=[FileAllowed(['jpg' , 'png'])])
    submit = SubmitField('Update')
    


 
    def validate_username(form,field):
       username = field.data
       user = User.query.filter_by(username = username).first()
       if user is not None:
        raise validators.ValidationError('Usuario ya existente!')

    def validate_email(form,field):
       email = field.data
       mailx = User.query.filter_by(email = email).first()
       if mailx is not None:
        raise validators.ValidationError('Correo electronico ya registrado!')

class Searched(FlaskForm):

    searched = TextAreaField('Searched',[validators.length(min=4,max=100)])
    submit = SubmitField('Update')        
        
      

class login(FlaskForm):
    
    username = TextAreaField('USERNAME',[validators.length(min=4,max=25, message='Ingresa un username valido' ),validators.DataRequired(message="El username es requerido")])
    password = PasswordField('PASSWORD',[validators.length(min=1,max=305, message='Ingresa una contraseña valida' ),validators.DataRequired(message="La contraseña es requerida")])
    note = TextAreaField('COMMENT')
    


class commentx(FlaskForm):
   comentario = TextAreaField('COMMENT')

class Forgot(FlaskForm):
  email = EmailField('Email address', [validators.DataRequired(), validators.Email()])

class ResetPass(FlaskForm):
  password = PasswordField('Password', [validators.DataRequired(),validators.Length(min = 4, max = 360)])
  confirm_password = PasswordField('Confirm Password', [validators.DataRequired(),validators.Length(min = 4, max = 360)])

class Postx(FlaskForm):


  title = StringField('Title', [validators.DataRequired()])
  content = CKEditorField('Content', [validators.DataRequired()])
  author = StringField('Author')
  slug = StringField('Slug', [validators.DataRequired()])
  submit = SubmitField('Submit')


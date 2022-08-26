from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('usuário', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('senha', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('lembrar-me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Email Inválido'), Length(max=50)])
    username = StringField('usuário', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('senha', validators=[InputRequired(), Length(min=8, max=80)])

class UpdatePasswordForm(FlaskForm):
    password = PasswordField('senha', validators=[InputRequired(), Length(min=8, max=80)])
    new_password = PasswordField('nova senha', validators=[InputRequired(), Length(min=8, max=80)])
    new_password_confirm = PasswordField('confirme a nova senha', validators=[InputRequired(), EqualTo('new_password', message='Senhas não combinam'), Length(min=8, max=80)])

class UpdateUsernameForm(FlaskForm):
    new_username = StringField('novo usuário', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('senha', validators=[InputRequired(), Length(min=8, max=80)])
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Lembrar-me')

class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email(message='E-mail Inválido'), Length(max=50)])
    username = StringField('Usuário', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max=80)])

class UpdatePasswordForm(FlaskForm):
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max=80)])
    new_password = PasswordField('Nova Senha', validators=[InputRequired(), Length(min=8, max=80)])
    new_password_confirm = PasswordField('Confirme a nova senha', validators=[InputRequired(), EqualTo('new_password', message='Senhas não combinam'), Length(min=8, max=80)])

class UpdateUsernameForm(FlaskForm):
    new_username = StringField('Novo usuário', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max=80)])
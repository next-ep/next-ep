from flask import render_template, redirect, flash, url_for
from flask_login import login_user, login_required, current_user, logout_user
from app.models import Serie, User
from app.forms import EditSerie, LoginForm, RegisterForm, RegisterSerie, UpdatePasswordForm, UpdateUsernameForm
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

from . import auth

@auth.route("/")
def index():
    return render_template("index.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('auth.index'))
        
        flash("Usuário ou senha incorretos", category="error")
        return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        if not User.query.filter_by(username=form.username.data).first() and\
        not User.query.filter_by(email=form.email.data).first():
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))
            
        flash("Erro ao cadastrar: Usuário ou Email já utilizados", category="warning")
        return redirect(url_for("auth.signup"))

    return render_template('signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/account/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = UpdatePasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        if user and \
        check_password_hash(current_user.password, form.password.data):
            hashed_password = generate_password_hash(form.new_password.data, method='sha256')
            user.password = hashed_password
            db.session.commit()
            logout_user()
            return redirect(url_for('auth.index'))
                
        flash("Erro ao alterar senha!", category="warning")
        return redirect(url_for('auth.change_password'))

    return render_template('change_password.html', form=form)

@auth.route('/account/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = UpdateUsernameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.get_id()).first()
        if user and \
        check_password_hash(current_user.password, form.password.data) and \
        not User.query.filter_by(username=form.new_username.data).first():
            user.username = form.new_username.data
            db.session.commit()
            return redirect(url_for('auth.index'))
        
        flash("Erro ao alterar o usuário!", category="warning")
        return redirect(url_for('auth.change_username'))
    return render_template('change_username.html', username=current_user.username, form=form)

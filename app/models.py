from email.policy import default
from flask_login import UserMixin
from app import db, login_manager
from sqlalchemy.orm import relationship

@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    series = relationship('Serie', backref="users")

class Serie(db.Model):
    __tablename__ = "serie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User')
    concluded = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

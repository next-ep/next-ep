from email.policy import default
from turtle import back
from flask_login import UserMixin
from app import db, login_manager
from sqlalchemy.orm import relationship

@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    private = db.Column(db.Boolean, unique=False, default=True)
    series = relationship('Serie', backref="user")

class Serie(db.Model):
    __tablename__ = "serie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False)
    serie_type = db.Column(db.String(255), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seasons = relationship('Season', backref="serie")
    concluded = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, name, serie_type, user_id):
        self.name = name
        self.user_id = user_id
        self.serie_type = serie_type

class Season(db.Model):
    __tablename__ = "season"
    id = db.Column(db.Integer, primary_key=True)
    season_number = db.Column(db.Integer)
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'))
    episodes = relationship('Episode', backref="season")
    concluded = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, season_number, serie_id):
        self.season_number = season_number
        self.serie_id = serie_id


class Episode(db.Model):
    __tablename__ = "episode"
    id = db.Column(db.Integer, primary_key=True)
    episode_number = db.Column(db.Integer)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    concluded = db.Column(db.Boolean, unique=False, default=False)

    def __init__(self, episode_number, season_id):
        self.episode_number = episode_number
        self.season_id = season_id

class Commentary(db.Model):
    __tablename__ = "commentary"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300))
    serie_id = db.Column(db.Integer, db.ForeignKey('serie.id'))
from flask_bootstrap import Bootstrap4
from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap4()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Realize o Login para conseguir acessar esse conteúdo.'

    from app import routes
    routes.init_app(app)

    return app
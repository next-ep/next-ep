from app.auth import auth as auth_blueprint
from app.series import series as series_blueprint

def init_app(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(series_blueprint)
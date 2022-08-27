from app.auth import auth as auth_blueprint

def init_app(app):
    app.register_blueprint(auth_blueprint)
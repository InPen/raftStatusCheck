# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.login_view = "auth.login"  # we'll create auth blueprint later
login_manager.login_message_category = "info"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # avoid circular imports
    from app.routes import main_bp
    # from app.auth import auth_bp  # later

    app.register_blueprint(main_bp)
    # app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

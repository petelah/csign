from dotenv import load_dotenv

load_dotenv()

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object("src.default_settings.app_config")

    migrate.init_app(app, db)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from src.commands import db_commands
    from src.users.routes import users
    from src.main.routes import main
    from src.errors.handlers import errors
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(db_commands)

    return app

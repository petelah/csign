from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_admin import Admin, AdminIndexView
from flask_migrate import Migrate
from os import getenv
from src.config import Config


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.admin:
                return True
            else:
                return False
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.home'))


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
admin = Admin(name='c-sign', index_view=MyAdminIndexView(), template_mode='bootstrap3')
migrate = Migrate()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    migrate.init_app(app, db)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)


    from src.users.routes import users
    from src.main.routes import main
    from src.errors.handlers import errors
    from src.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(main)

    return app

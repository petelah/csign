from datetime import datetime
from src import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    business_name = db.Column(db.String(120), unique=True, nullable=False)
    business_url = db.Column(db.String(200), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    post_code = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(10), nullable=False)
    menu_url = db.Column(db.String(200), unique=True, nullable=True)
    menu_file = db.Column(db.String(20), nullable=True, default='default.png')
    logo = db.Column(db.String(20), nullable=False, default='default.jpg')
    qr_image = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    verified = db.Column(db.Boolean, nullable=True, default=False)
    admin = db.Column(db.Boolean, nullable=True, default=False)
    sign_ins = db.relationship('SignIn', backref='user_id')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.first_name}', '{self.email}')"


class SignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    signup = db.Column(db.Boolean, nullable=True, default=True)
    symptoms = db.Column(db.Boolean, nullable=False, default=False)
    date_sign = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    business_id = db.Column(db.Integer, db.ForeignKey('user.id'))

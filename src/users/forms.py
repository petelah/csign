from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.models import User
from flask_login import current_user
from wtforms_components import SelectField


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    business_name = StringField('Business Name',
                           validators=[DataRequired(), Length(min=2, max=120)])
    first_name = StringField('First Name',
                                validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('last Name',
                                validators=[DataRequired(), Length(min=2, max=30)])
    phone_number = StringField('Phone Number',
                                validators=[DataRequired(), Length(min=8, max=15)])
    address = StringField('Address',
                                validators=[DataRequired(), Length(min=2, max=120)])
    post_code = IntegerField('Post Code',
                                validators=[DataRequired()])
    state = SelectField(u'State:',
                        choices=[('nsw', 'NSW'),
                                 ('act', 'ACT'),
                                 ('tas', 'TAS'),
                                 ('nt', 'NT'),
                                 ('wa', 'WA'),
                                 ('qld', 'QLD')])
    # add file upload after mvp
    # menu_file = FileField('Menu File', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'pdf'])])
    menu_url = StringField('Link to online menu',
                                validators=[Length(min=2, max=200)],
                           render_kw={"placeholder": "http://wwww.example.com/menu"})
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')

    def validate_business_name(self, business_name):
        user = User.query.filter_by(business_name=business_name.data).first()
        if user:
            raise ValidationError('Username in use, please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email in use, please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    business_name = StringField('Business Name',
                           validators=[DataRequired(), Length(min=2, max=120)])
    business_url = StringField('Sign in link "c-sign.in/signin/<link>"',
                           validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    menu_url = StringField('Link to online menu',
                           validators=[Length(min=2, max=200)])
    logo = FileField('Update Logo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_business_name(self, business_name):
        if business_name.data != current_user.business_name:
            user = User.query.filter_by(business_name=business_name.data).first()
            if user:
                raise ValidationError('Business name in use, please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email in use, please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class SignInForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('last Name',
                            validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    business_name = StringField('Business Name',
                           validators=[DataRequired(), Length(min=2, max=120)])
    phone_number = StringField('Phone Number',
                                validators=[DataRequired(), Length(min=8, max=15)])
    symptoms = BooleanField('I am not experiencing any flu like symptoms:', validators=[DataRequired()])
    sign_up = BooleanField('Want cool emails from this place?')
    submit = SubmitField('Sign In')
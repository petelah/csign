from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.models import User
from flask_login import current_user
from wtforms_components import SelectField
from src.services import check_api_valid


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    business_name = StringField('Business Name',
                           validators=[DataRequired(), Length(min=2, max=120)])
    first_name = StringField('First Name',
                                validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name',
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
            raise ValidationError('Business name in use, please choose a different one.')

    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(phone_number=phone_number.data).first()
        if user:
            raise ValidationError('Phone number in use, please choose a different one.')

    def validate_address(self, address):
        user = User.query.filter_by(address=address.data).first()
        if user:
            raise ValidationError('Address name in use, please choose a different one.')

    def validate_menu_url(self, menu_url):
        user = User.query.filter_by(menu_url=menu_url.data).first()
        if user:
            raise ValidationError('URL in use, please choose a different one.')

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
    api_key = StringField('Mailchimp API Key', validators=[Length(max=300)])
    logo = FileField('Update Logo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_api_key(self, api_key):
        if api_key.data:
            if not check_api_valid(api_key.data):
                raise ValidationError('Please use a valid API key.')

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
    submit = SubmitField('Change Password')


class SignInForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('last Name',
                            validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = TelField('Phone Number',
                                validators=[DataRequired(), Length(min=8, max=15)])
    symptoms = BooleanField('I am not experiencing any flu like symptoms:', validators=[DataRequired()])
    sign_up = BooleanField('Want cool emails from this place?')
    submit = SubmitField('Sign In')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=90)],
                       render_kw={"placeholder": "Name"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email"})
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1200)],
                            render_kw={"placeholder": "Message"})
    submit = SubmitField('Send')

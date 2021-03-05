from flask import render_template, request, Blueprint, flash, redirect, url_for, make_response, current_app
from src.models import SignIn, User
from src import db
from src.users.forms import SignInForm, ContactForm
from src.services import business_url_return, EmailService, create_cookie, grab_cookie
from src.users.decorators import verify_business

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        if current_app.config["FLASK_ENV"] == 'production':
            body_html = render_template(
                'mail/user/contact_email.html',
                name=form.name.data,
                message=form.message.data,
                email=form.email.data
            )
            body_text = render_template(
                'mail/user/contact_email.txt',
                name=form.name.data,
                message=form.message.data,
                email=form.email.data
            )
            EmailService.email('admin@c-sign.in', 'New message.', body_html, body_text)
        return render_template('success.html', type='email')
    return render_template('contact.html', title='Contact Us', form=form)


@main.route("/signin/<string:business_name>", methods=['GET', 'POST'])
@verify_business
def sign_in(business_name):
    """
    Main sign in function.
    Will search the database for existing business taken from the url, if not found will return 404.
    If user has previously signed in within the last 4 hours they will not need to sign in again as a
    cookie will store their previous login.
    :param business_name:
    :return:
    """
    req = request
    business = User.query.filter_by(business_url=business_name).first_or_404()
    logo = url_for('static', filename='profile_pics/' + business.logo)
    form = SignInForm()
    if form.validate_on_submit():
        new_sign_in = SignIn(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            phone=form.phone_number.data,
            symptoms=form.symptoms.data,
            signup=form.sign_up.data,
            user_id=business
        )
        db.session.add(new_sign_in)
        db.session.commit()
        if business.menu_url is not None:
            bu = business_url_return(business.menu_url)
            res = make_response(redirect(bu))
            # Set sign in to 4 hours so guest can re-scan the code
            res.set_cookie(business_name, 'signed_in', secure=True, max_age=60 * 60 * 4)
            if not request.cookies.get('csign'):
                create_cookie(res, form)
            return res
        else:
            flash('You have been signed in!', 'success')
            return render_template('signin.html', logo=logo, business_name=business_name, form=form)

    elif request.method == 'GET':
        if request.cookies.get('csign'):
            # pull cookie information
            grab_cookie(form, request)
        if request.cookies.get(business_name):
            if business.menu_url is not None:
                bu = business_url_return(business.menu_url)
                res = make_response(redirect(bu))
                return res
        return render_template('signin.html', logo=logo, business_name=business.business_name, form=form)
    return render_template('signin.html', logo=logo, business_name=business.business_name, form=form)

from flask import render_template, request, Blueprint, flash, redirect, url_for, abort, make_response
from datetime import datetime
from src.models import SignIn, User
from src import db
from src.users.forms import SignInForm, ContactForm
from src.users import send_contact_email, business_url_return

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/home2")
def home2():
    return render_template('home2.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_contact_email(
            form.name.data,
            form.email.data,
            form.message.data
        )
        return render_template('success.html', type='email')
    return render_template('contact.html', title='Contact Us', form=form)


@main.route("/signin/<string:business_name>", methods=['GET', 'POST'])
def sign_in(business_name):
    """
    Main sign in function.
    Will search the database for existing business taken from the url, if not found will return 404.
    If user has previously signed in within the last 4 hours they will not need to sign in again as a
    cookie will store their previous login.
    :param business_name:
    :return:
    """
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
            res.set_cookie(business_name, 'signed_in', secure=True, max_age=60 * 60 * 4)
            if not request.cookies.get('csign'):
                res.set_cookie('csign', 'signed_in', secure=True, max_age=60 * 60 * 24 * 365 * 1)
                res.set_cookie('csign-email', form.email.data, secure=True, max_age=60 * 60 * 24 * 365 * 1)
                res.set_cookie('csign-fname', form.first_name.data, secure=True, max_age=60 * 60 * 24 * 365 * 1)
                res.set_cookie('csign-lname', form.last_name.data, secure=True, max_age=60 * 60 * 24 * 365 * 1)
                res.set_cookie('csign-phone', form.phone_number.data, secure=True, max_age=60 * 60 * 24 * 365 * 1)
            return res
        else:
            flash('You have been signed in!', 'success')
            return render_template('signin.html', logo=logo, business_name=business_name, form=form)

    elif request.method == 'GET':
        bu = business_url_return(business.menu_url)
        res = make_response(redirect(bu))
        return res
        if request.cookies.get('csign'):
            # pull cookie information
            form.email.data = request.cookies.get('csign-email')
            form.first_name.data = request.cookies.get('csign-fname')
            form.last_name.data = request.cookies.get('csign-lname')
            form.phone_number.data = request.cookies.get('csign-phone')
        if request.cookies.get(business_name):
            if business.menu_url is not None:
                bu = business_url_return(business.menu_url)
                res = make_response(redirect(bu))
                return res
        return render_template('signin.html', logo=logo, business_name=business.business_name, form=form)
    return render_template('signin.html', logo=logo, business_name=business.business_name, form=form)

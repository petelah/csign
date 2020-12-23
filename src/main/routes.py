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
    form = SignInForm()
    business = User.query.filter_by(business_url=business_name).first_or_404()
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
            res.set_cookie(business_name, 'signed_in', max_age=60 * 1)
            return res
        else:
            flash('You have been signed in!', 'success')
            return render_template('signin.html', logo=logo, business_name=b_name, form=form)

    elif request.method == 'GET':
        if request.cookies.get(business_name):
            if business.menu_url is not None:
                bu = business_url_return(business.menu_url)
                res = make_response(redirect(bu))
                return res
        logo = url_for('static', filename='profile_pics/' + business.logo)
        b_name = business.business_name
        return render_template('signin.html', logo=logo, business_name=b_name, form=form)
    logo = url_for('static', filename='profile_pics/' + business.logo)
    b_name = business.business_name
    return render_template('signin.html', logo=logo, business_name=b_name, form=form)

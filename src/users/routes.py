from flask import render_template, url_for, flash, redirect, request, Blueprint, send_from_directory, abort, current_app
from src import db, bcrypt
from src.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm)
from src.services import save_picture, save_csv, EmailService, generate_qr, strip_chars, Encryption
from src.models import User
from flask_login import login_user, current_user, logout_user, login_required
import os

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data,
                    business_name=form.business_name.data,
                    business_url=strip_chars(form.business_name.data),
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    phone_number=form.phone_number.data,
                    address=form.address.data,
                    post_code=form.post_code.data,
                    state=form.state.data,
                    menu_url=form.menu_url.data,
                    qr_image=generate_qr(form.business_name.data),
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        if current_app.config['FLASK_ENV'] == 'production':
            EmailService.send_confirm_email(form.first_name.data, form.email.data)
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Login not found. Please check email and password', 'danger')
    return render_template('login.html', title='login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.logo.data:
            picture_file = save_picture(form.logo.data)
            current_user.logo = picture_file
        current_user.menu_url = form.menu_url.data
        current_user.business_url = strip_chars(form.business_url.data).lower()
        current_user.email = form.email.data
        current_user.business_name = form.business_name.data
        if form.api_key.data:
            current_user.mail_api = Encryption.encrypt_user_data(form.api_key.data.encode())
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.business_name.data = current_user.business_name
        form.menu_url.data = current_user.menu_url
        form.business_url.data = current_user.business_url
        form.email.data = current_user.email
        if current_user.mail_api:
            form.api_key.data = Encryption.decrypt_user_data(current_user.mail_api).decode()
        else:
            form.api_key.data = current_user.mail_api
    logo = url_for('static', filename='profile_pics/' + current_user.logo)
    # Serve files from cloudfront if server is in production
    if current_app.config["FLASK_ENV"] == 'production':
        qr_file = f'https://ddjesgdltvd54.cloudfront.net/qr_codes/{current_user.qr_image}'
    else:
        qr_file = url_for('static', filename='qr_codes/' + current_user.qr_image)
    return render_template('account.html', title='Account', logo=logo, qr_file=qr_file, form=form)


@users.route("/account/change_password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db.session.commit()
        return redirect(url_for('users.account'))
    return render_template('change_password.html', form=form)


@users.route("/download-csv")
@login_required
def download_csv():
    try:
        filename = save_csv(current_user.id)
        return send_from_directory(os.path.join(os.getcwd(),current_app.config["CSV_FOLDER"]), filename=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        EmailService.send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expired', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has now been updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

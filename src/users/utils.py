from flask import url_for, current_app
from src import mail, db
from flask_mail import Message
import secrets
import os
from PIL import Image
import qrcode
import re
from threading import Thread
from src.models import SignIn, User
import csv
from src.config import Config
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from cryptography.fernet import Fernet


def strip_chars(business_name):
    regex = re.compile("[A-Za-z0-9]")
    return_matched = regex.findall(business_name)
    return ''.join(return_matched).lower()


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    #form_picture.save(picture_path)

    return picture_fn


def generate_qr(business_name):
    img = qrcode.make('http://c-sign.in/signin/' + strip_chars(business_name))
    random_hex = secrets.token_hex(8)
    picture_fn = business_name + random_hex + '.png'
    picture_path = os.path.join(current_app.root_path, 'static/qr_codes', picture_fn)
    img.save(picture_path)

    return picture_fn


def send_qr_email():
    pass


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_contact_email(name, email, message):
    msg = Message(f'Contact email from {name}',
                  sender=email,
                  reply_to=email,
                  recipients=['admin@c-sign.in'])
    msg.body = f"""{message}"""
    app = current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then ignore this email.    
    '''
    mail.send(msg)


def save_csv(id):
    random_hex = secrets.token_hex(8)
    filename = f"{id}-{random_hex}.csv"
    save_path = os.path.join(Config.CSV_FOLDER, filename)
    sign_ins = SignIn.query.filter_by(business_id=id, signup=True).all()
    save_list = []
    for obj in sign_ins:
        save_list.append(obj.email)
    save_list = set(save_list)
    print("working")
    with open(save_path, 'w', newline='') as csvfile:
        signinwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        signinwriter.writerow(['Email'])
        for email in save_list:
            signinwriter.writerow([email])
    print("got to end")
    return filename


def check_api_valid(api_key):
    if '-' not in api_key:
        return False
    server = api_key.split('-')
    client = MailchimpMarketing.Client()
    client.set_config({
        "api_key": api_key, "server": server[1]
    })
    try:
        response = client.ping.get()
        if response['health_status'] == "Everything's Chimpy!":
            return True
    except ApiClientError:
        return False


def encrypt_user_data(data):
    return Fernet(Config.API_SECRET_KEY).encrypt(data)


def decrypt_user_data(data):
    convert = bytes.fromhex(data[2::])
    return Fernet(Config.API_SECRET_KEY).decrypt(convert)


def business_url_return(business_menu_url, **kwargs):
    bu = business_menu_url
    if bu.find("http://") != 0 and bu.find("https://") != 0:
        bu = "http://" + bu
    return bu


def cookie_maker():
    pass


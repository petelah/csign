from flask import url_for, current_app
from src import mail
from flask_mail import Message
from threading import Thread


class EmailService:

    @staticmethod
    def send_qr_email():
        pass

    @staticmethod
    def send_async_email(app, msg):
        with app.app_context():
            mail.send(msg)

    @staticmethod
    def send_contact_email(name, email, message):
        msg = Message(f'Contact email from {name}',
                      sender=email,
                      reply_to=email,
                      recipients=['admin@c-sign.in'])
        msg.body = f"""{message}"""
        app = current_app._get_current_object()
        Thread(target=send_async_email, args=(app, msg)).start()

    @staticmethod
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

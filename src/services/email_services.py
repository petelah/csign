from flask import url_for, current_app, render_template
from threading import Thread
import boto3


class EmailService:

    @staticmethod
    def send_qr_email():
        pass

    @staticmethod
    def send_async_email(app, msg):
        pass

    @staticmethod
    def send_reset_email(user):
        token = user.issue_token()
        body_html = render_template(
            'mail/user/reset_password.html',
            name=user.first_name,
            token=token,
            email=user.email
        )
        body_text = render_template(
            'mail/user/reset_password.txt',
            name=user.first_name,
            token=token,
            email=user.email
        )
        EmailService.email(user.email, 'Password Reset', body_html, body_text)

    @staticmethod
    def send_confirm_email(user):
        token = user.issue_token()
        body_html = render_template(
            'mail/user/join_email.html',
            name=user.first_name,
            token=token,
        )
        body_text = render_template(
            'mail/user/join_email.txt',
            name=user.first_name,
            token=token,
        )
        EmailService.email(user.email, 'Welcome to C-Sign!', body_html, body_text)

    @staticmethod
    def email(to_email, subject, body_html, body_text):
        client = boto3.client('ses', region_name='ap-southeast-2')
        return client.send_email(
            Source='noreply@c-sign.in',
            Destination={
                'ToAddresses': [
                    to_email,
                ]
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': body_html,
                        'Charset': 'UTF-8'
                    },
                }
            }
        )
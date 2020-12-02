from os import getenv

class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    MAIL_DEFAULT_SENDER = 'seabrook.peter@gmail.com'
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_PORT = getenv('MAIL_PORT')
    MAIL_USE_TLS = getenv('MAIL_USE_TLS')
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    FLASK_ADMIN_SWATCH = 'cerulean'
    AWS_BUCKET = 'csigncsv'
    AWS_CONTENT_URL = 'https://s3-ap-southeast-2.amazonaws.com/'
    UPLOAD_FOLDER = 'static/images'
    CSV_FOLDER = 'src/static/csv'
    S3_CSV_FOLDER = 'static/csv'
    IMAGE_URL = 'images'
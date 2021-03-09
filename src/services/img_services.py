import secrets
import os
from pathlib import Path
from PIL import Image
from flask import current_app
import qrcode
from .general_services import strip_chars
from .file_services import FileService


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def generate_qr(business_name):
    qr_dir = Path.cwd().joinpath("src", "static", "qr_codes")
    if not qr_dir.exists():
        qr_dir.mkdir(parents=True, exist_ok=True)

    stripped_name = strip_chars(business_name)
    img = qrcode.make('http://c-sign.in/signin/' + stripped_name)
    if current_app.config['FLASK_ENV'] == 'production':
        picture_fn = FileService.save_qr(img, '.png', business_name)
    else:
        random_hex = secrets.token_hex(8)
        picture_fn = stripped_name + random_hex + '.png'
        picture_path = os.path.join(os.getcwd(), 'src/static/qr_codes', picture_fn)
        img.save(picture_path)

    return picture_fn

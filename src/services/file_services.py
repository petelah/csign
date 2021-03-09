import boto3
import secrets
import os
import logging
import io
import csv

from botocore.exceptions import ClientError
from flask import current_app
from PIL import Image
from src.models import SignIn
from threading import Thread
from time import sleep
from pathlib import Path


class FileService:
    s3 = boto3.resource('s3')

    @staticmethod
    def local_storage(img, dir, filename):
        path = os.path.join('src/static/', dir, filename)
        img.save(path)

    @staticmethod
    def strip_exif(img, s3=None):
        image = Image.open(img)

        data = list(image.getdata())
        no_exif_img = Image.new(image.mode, image.size)
        no_exif_img.putdata(data)
        if s3:
            in_mem_file = io.BytesIO()
            no_exif_img.save(in_mem_file, format=image.format)
            in_mem_file.seek(0)
            return in_mem_file

        return no_exif_img

    @classmethod
    def image_save(cls, img, suffix, id, dir):
        # Generate a id + hexed filename
        filename = str(id) + '-' + secrets.token_hex(32) + suffix
        img = cls.strip_exif(img, True)
        if current_app.config["AWS_S3_BUCKET"]:
            try:
                cls.s3.Bucket(current_app.config["AWS_S3_BUCKET"]).put_object(
                    Key=current_app.config["S3_FOLDER"] + os.path.join(dir, filename),
                    Body=img
                )
                return filename
            except ClientError as e:
                # log error here
                logging.warning(e)
                print(e)
        else:
            cls.local_storage(img, dir, filename)
            return filename
        return None

    @classmethod
    def save_qr(cls, img, suffix, business_name):
        # Generate a id + hexed filename
        filename = business_name + '-' + secrets.token_hex(8) + suffix
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format="PNG")
        img_byte_array = img_byte_array.getvalue()
        try:
            cls.s3.Bucket(current_app.config["AWS_S3_BUCKET"]).put_object(
                Key=os.path.join('qr_codes', filename),
                Body=img_byte_array
            )
            return filename
        except ClientError as e:
            # log error here
            logging.warning(e)
            print(e)
        return None

    @classmethod
    def file_store(cls):
        pass


def save_csv(id):
    csv_dir = Path.cwd().joinpath("src", "static", "csv")
    if not csv_dir.exists():
        csv_dir.mkdir(parents=True, exist_ok=True)

    random_hex = secrets.token_hex(8)
    filename = f"{id}-{random_hex}.csv"
    save_path = os.path.join(os.getcwd(), 'src/static/csv', filename)
    sign_ins = SignIn.query.filter_by(business_id=id, signup=True).all()
    save_list = []
    for obj in sign_ins:
        save_list.append(obj.email)
    save_list = set(save_list)
    with open(save_path, 'w', newline='') as csvfile:
        signinwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        signinwriter.writerow(['Email'])
        for email in save_list:
            signinwriter.writerow([email])
    Thread(target=csv_delete, args=(filename,)).start()
    return filename


def csv_delete(filename):
    sleep(20)
    os.remove(os.path.join(
        os.getcwd(), 'src/static/csv', filename
    ))

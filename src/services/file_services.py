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
    def file_store(cls):
        pass


def save_csv(id):
    random_hex = secrets.token_hex(8)
    filename = f"{id}-{random_hex}.csv"
    save_path = os.path.join(Config.CSV_FOLDER, filename)
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
    return filename


def csv_delete():
    pass
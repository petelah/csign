from cryptography.fernet import Fernet
from flask import current_app


class Encryption:
    @staticmethod
    def encrypt_user_data(data):
        return Fernet(current_app.config["API_SECRET_KEY"]).encrypt(data)

    @staticmethod
    def decrypt_user_data(data):
        convert = bytes.fromhex(data[2::])
        return Fernet(current_app.config["API_SECRET_KEY"]).decrypt(convert)

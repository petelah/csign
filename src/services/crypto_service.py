from cryptography.fernet import Fernet
from src.config import Config


class Encryption:
    @staticmethod
    def encrypt_user_data(data):
        return Fernet(Config.API_SECRET_KEY).encrypt(data)

    @staticmethod
    def decrypt_user_data(data):
        convert = bytes.fromhex(data[2::])
        return Fernet(Config.API_SECRET_KEY).decrypt(convert)

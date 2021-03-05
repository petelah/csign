from flask import Blueprint, current_app
from src.services import generate_qr, strip_chars

from src import db

db_commands = Blueprint("db-custom", __name__)


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("DB Created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    db.engine.execute("DROP TABLE IF EXISTS alembic_version;")
    print("Tables deleted")


@db_commands.cli.command("seed")
def seed_db():
    from src.models import User, SignIn
    from src import bcrypt
    from faker import Faker
    import random

    faker = Faker()
    users = []
    TEST_PASSWORD = '123456'

    if not TEST_PASSWORD:
        raise ValueError('TEST_PASSWORD not provided.')

    websites = ['www.facebook.com', 'www.microsoft.com', 'www.instagram.com', 'www.reddit.com', 'www.gmail.com', 'www.bing.com', 'www.excel.com']

    for i in range(5):
        # Add users
        user = User()
        user.email = f"test{i}@test.com"
        user.business_name = f"test{i}"
        user.business_url = strip_chars(user.business_name)
        user.username = f"test{i}"
        user.menu_url = websites[i]
        user.first_name = faker.first_name()
        user.last_name = faker.last_name()
        user.phone_number = faker.msisdn()
        user.address = faker.address()
        user.state = "NSW"
        user.post_code = "2222"
        user.verified = True
        user.qr_image = generate_qr(user.business_name)
        user.password = bcrypt.generate_password_hash(f"{TEST_PASSWORD}").decode("utf-8")
        db.session.add(user)
        users.append(user)

    user = User()
    user.email = f"test10@test.com"
    user.business_name = f"test10"
    user.business_url = strip_chars(user.business_name)
    user.username = f"test10"
    user.menu_url = websites[-1]
    user.first_name = faker.first_name()
    user.last_name = faker.last_name()
    user.phone_number = faker.msisdn()
    user.address = faker.address()
    user.state = "NSW"
    user.post_code = "2222"
    user.verified = False
    user.qr_image = generate_qr(user.business_name)
    user.password = bcrypt.generate_password_hash(f"{TEST_PASSWORD}").decode("utf-8")
    db.session.add(user)
    users.append(user)

    db.session.commit()
    print("Users Added")

    for i in range(25):
        sign_in = SignIn()
        sign_in.email = f"test{i}@test.com"
        sign_in.first_name = faker.first_name()
        sign_in.last_name = faker.last_name()
        sign_in.phone = faker.msisdn()
        sign_in.symptoms = True
        sign_in.signup = random.choice([True, False])
        sign_in.business_id = random.choice(users).id
        db.session.add(sign_in)

    db.session.commit()

    print("Sign in's added")
    print("Tables seeded")

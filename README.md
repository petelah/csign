# C-Sign.in

A fully featured covid sign in solution for all types of businesses.

It allows your redirect straight after sign in to another page ie: a menu, ordering or info page 
for your business.

## Features
 - User/business sign up, upon signup the back end will generate a qr code and unique url 
 used for scanning and signing in.
 - Password reset/user verification.
 - Change url function if for some reason you don't like your generated url.
 - Download CSV of signed up emails for each individual user/business.
 - Admin panel.
 - Remembers users sign in credentials for fast sign in at venues.
 - Holds sign in information for 4 hours so the same QR code can be used in venues if 
 people use it to get to the menu, no need for multiple codes.

## Requirements
Main requirements are:
 - Python 3.7+
 - Flask - The web framework everything is built on top of.
    - Flask-Migrate - Used for updating our database changes safely.
    - Flask-Login - Our login system based on sessions and tokens.
    - Flask-SQLAlchemy - A binder for the SQLAlchemy package for flask integration.
    - Flask-WTForms - A binder for the WTForms package for flask integration.
    - Flask-Bcrypt - Binder for Bcrypt password hashing for flask integration.
 - SQLAlchemy - Our ORM of choice for interfacing and sanitising SQL inputs.
 - Boto3 - Amazon AWS interfacing client used for S3 uploads and SES mail system
 - Gunicorn - WSGI wrapper for flask.
 - Mailchimp-marketing - API wrapper for Mailchimp integration to allow users to add their API keys to their accounts.
 - Pillow - Powerful fully featured imaging package for image manipulation.
 - WTForms - Form sanitisation and input manager.
 - Qrcode - A package for generating qr codes for users businesses.
 - Python-dotenv - Environment file loading.
 - Jinja2 - HTML templating package.
 - Cryptography - Powerful cryptography package for encrypting and decrypting the database.
 - Faker - Dummy data generation for rapid testing
 - Bcrypt - Password hashing
 - Autopep8 - Code linting to PEP8 standards
 - Pyscopg2 - SQL data connection parsing for postgres databases.
 
 Anything else listed in requirements are extra dependant packages used by the above packages
 
The rest can be installed via requirements.txt


## Installation
Fill out your .env file and place it in src folder, an example is provided.

To use full functionality ie: AWS S3 and SES you will need to create a new IAM user and give it access to your 
chosen bucket and SES account.

Please note with SES you will need to verify the emails you want to send and receive from as AWS starts you out 
in the sandbox, you can request production upgrade if you wish to run this without the sandbox.

Testing Environment:
Make sure you FLASK_ENV is set to 'testing'. Please note that you will not be able to send emails to verify accounts 
while in testing so an admin account will need to verify users manually. Such account is provided in the seeding of the databse 
for testing purposes.
Files will also be locally stored versus in an S3 bucket when testing locally.

Production Environment:
You will need to have your AWS IAM setup as stated above and credentials in your .env file and set your production db accordingly.
FLASK_ENV will need to be set to 'production'.


__Local:__

```shell script
docker-compose up
```

__Deployment:__
This is designed to be run through the pipeline of: Github actions -> build image -> push to AWS ECR -> update service 
on ECS.
There are many other cloud providers you could run this on but it would require you to decouple from AWS integration and 
is not advised.
# C-Sign.in

A fully featured covid sign in solution for all types of businesses.

It allows your redirect straight after sign in to another page ie: a menu, ordering or info page 
for your business.

## Features
 - User/business sign up, upon signup the back end will generate a qr code and unique url 
 used for scanning and signing in.
 - Password reset
 - Change url function if for some reason you don't like your generated url
 - Download CSV of signed up emails for each individual user/business
 - Admin panel
 - Remembers users sign in credentials for fast sign in at venues
 - Holds sign in information for 4 hours so the same QR code can be used in venues if 
 people use it to get to the menu, no need for multiple codes.

## Requirements
Main requirements are:
 - Python 3.7+
 - Flask
 - Postgres
 
The rest can be installed via requirements.txt


## Installation

C-Sign is designed to be installed and run on an EC2 instance.
For a great guide on how to get setup and run EC2 with postgres check out: 
[EC2 Guide by Colin Forster]: https://github.com/Ctrain68/EC2_postgres_sql_guide

The easiest way to run this going to be fork and edit the actions with your postgres server address 
and 
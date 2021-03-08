#!/bin/sh

export FLASK_APP=run.py

#flask db-custom create
#flask db-custom seed

if flask db-custom check | grep -q '1'; then
  echo "yes"
  flask db upgrade
else
  flask db-custom create
  flask db-custom seed
  flask db init
  flask db migrate -m "first migration"
  flask db upgrade
fi

gunicorn -w 2 --bind 0.0.0.0:5000 run:app

# Pull python
FROM python:3.8-slim

# Create working dir
RUN mkdir /app

# Copy files over
COPY run.py /app
COPY wait.sh /app
COPY init.sh /app
COPY requirements.txt /app
COPY src/ /app/src/

# Make working dir app
WORKDIR /app

#Update alpine and python
# RUN apt-get update && apt-get install -y postgresql-client

# Upgrade pip
RUN pip3 install --upgrade pip

# Install requirements
RUN pip3 install -r requirements.txt

# Environment vars
ENV FLASK_APP=run.py
ENV FLASK_DEBUG=0

# Expose working port
EXPOSE 5000

# CMD ./init.sh
# CMD flask db upgrade
CMD gunicorn -w 2 --bind 0.0.0.0:5000 run:app
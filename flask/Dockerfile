# FROM ubuntu:16.04
# RUN apt-get update
# RUN apt-get install -y python3 python3-dev python3-pip

# Use the Python3.7.2 image
FROM python:3.7.2-stretch

# LABEL maintainer="Rohit Bhore <rohitpbhore@gmail.com>"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app 
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]
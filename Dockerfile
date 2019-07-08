# pull official base image
FROM python:3.7-alpine

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /app
RUN mkdir /config_file

# copy app
COPY . /app/

# Set the working directory to /app
WORKDIR /app

# install the requirements
RUN pip install -r requirements.txt

RUN rm -rf /root/.cache/pip/

# run entrypoint.sh
ENTRYPOINT ["python", "configtree_to_file.py"]
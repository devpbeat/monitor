# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk --no-cache add \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    gettext \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    git \
    curl

#timezone configuration
RUN echo "America/Asuncion" > /etc/timezone

# install dependencies
RUN pip install --upgrade pip
COPY ./backend/requirements.txt /code/
RUN pip install -r requirements.txt

# copy project
COPY ./backend/ /code/

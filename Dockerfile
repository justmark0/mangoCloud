FROM python:3.9

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir /mangoCloud

WORKDIR /mangoCloud
COPY mangoCloud /mangoCloud
VOLUME /files
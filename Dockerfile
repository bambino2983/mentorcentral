FROM python:3.9.6-alpine


ADD . /mentorcentral
WORKDIR /mentorcentral

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

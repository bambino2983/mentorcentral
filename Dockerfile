FROM python:3.6.8


ADD . /mentorcentral
WORKDIR /mentorcentral

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

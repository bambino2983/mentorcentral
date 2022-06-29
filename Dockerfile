FROM python:3.6.8-alpine
RUN pip install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/entrypoint.sh"]


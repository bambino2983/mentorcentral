FROM python:3.6.8-alpine
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

ENTRYPOINT ["sh", "/entrypoint.sh"]


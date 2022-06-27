FROM python:3.9.6-alpine
RUN pip install --upgrade pip

COPY ./requirements.txt
RUN pip install -r requirements.txt

COPY ./centralmentor /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
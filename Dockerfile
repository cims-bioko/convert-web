FROM tiangolo/meinheld-gunicorn:python3.6-alpine3.8
LABEL maintainer="brent.atkinson@gmail.com"

EXPOSE 80

COPY ./convert_web /app/convert_web
COPY ./run.py /app/main.py

COPY requirements.txt /tmp/

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt

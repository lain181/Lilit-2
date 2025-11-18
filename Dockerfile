FROM python:3.13-alpine3.19
COPY requirements.txt /temp/requirements.txt
COPY lilit /lilit
WORKDIR /lilit
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password star

USER star


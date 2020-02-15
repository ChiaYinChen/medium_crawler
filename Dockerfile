FROM python:3.7.6-alpine
MAINTAINER chiayinchen
WORKDIR /
RUN mkdir /medium_crawler
COPY . /medium_crawler
RUN apk add --no-cache --update tzdata git vim curl

ENV TZ=Asia/Taipei
ENV VISUAL=vim

RUN pip install --no-cache-dir --upgrade pip pipenv
RUN (cd /medium_crawler && pipenv install)

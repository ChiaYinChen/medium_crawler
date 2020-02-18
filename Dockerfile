FROM python:3.7.6-alpine
MAINTAINER chiayinchen
WORKDIR /
RUN mkdir /medium_crawler
COPY . /medium_crawler
RUN apk add --no-cache --update tzdata git vim curl python3-dev openssl-dev \
  libffi-dev libxml2-dev libxslt-dev gcc ca-certificates musl-dev

ENV TZ=Asia/Taipei
ENV VISUAL=vim

RUN pip3 install --no-cache-dir --upgrade pip pipenv
RUN (cd /medium_crawler && pipenv install)

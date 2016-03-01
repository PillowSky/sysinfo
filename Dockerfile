# sysinfo with Debian:jessie

FROM        debian:jessie
MAINTAINER  PillowSky <pillowsky@qq.com>

RUN apt-get update \
&&  apt-get install -y python python-flask \
&&  apt-get clean \
&&  rm -rf /var/lib/apt/lists/* \
&&  mkdir /app

ADD . /app
WORKDIR /app

ENV LABEL Dockerfile
ENV PORT 8000

EXPOSE $PORT

USER daemon
CMD ["python", "client.py"]
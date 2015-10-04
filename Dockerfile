FROM ubuntu:14.04
MAINTAINER Mikhail Kuznetsov <mkuznetsov.dev@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV INITRD No

RUN locale-gen ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN ulimit -n 1024 \
&& apt-get update -y \
&& apt-get update -y --fix-missing \
&& apt-get -y install git wget python-dev libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev \
tcl8.6-dev tk8.6-dev python3-tk

RUN wget https://bootstrap.pypa.io/ez_setup.py && python ez_setup.py && wget https://bootstrap.pypa.io/get-pip.py \
&& python get-pip.py

RUN groupadd -r django && useradd -r -g django django

ADD requirements /app/requirements
RUN pip install -r /app/requirements/local.txt
ENV DJANGO_SETTINGS_MODULE app_marvel.settings.local

WORKDIR /app
EXPOSE 8000
RUN mkdir -p /app && \
     touch /app/.keep && \
     chown -R django:django /app
VOLUME ["/app"]
USER django
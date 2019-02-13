FROM alpine:latest

MAINTAINER Carlos Eduardo Colón Rangel
LABEL maintainer="espacio.sideral@gmail.com"

ENV LANG en_US.utf8

RUN apk add --update bash python3 ansible git \
 && rm -rf /var/cache/apk/*

WORKDIR /src

COPY . .

ADD ./ssh/id_rsa /root/.ssh/id_rsa
ADD ./ssh/id_rsa.pub /root/.ssh/id_rsa.pub
ADD ./ssh/known_hosts /root/.ssh/known_hosts

RUN ln -s /usr/bin/python3 /usr/bin/python \
 && chmod 600 /root/.ssh/id_rsa \
 && chmod 600 /root/.ssh/id_rsa.pub \
 && chmod 600 /root/.ssh/known_hosts \
 && python /src/setup.py install

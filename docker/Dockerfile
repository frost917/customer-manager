﻿FROM alpine/git AS clone

RUN git clone https://github.com/frost917/customer-manager.git /customer-manager

FROM python:3.8-slim-buster AS dev

ENV LC_CTYPE=ko_KR.UTF-8 \
    LC_TIME=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8

RUN apt update && apt install -y locales git \
    && locale-gen \
    && dpkg-reconfigure locales

COPY --from=clone /customer-manager /customer-manager

WORKDIR /customer-manager

RUN pip install --no-cache-dir -r requirements.txt

CMD tail -f /dev/null
﻿FROM alpine/git AS clone

RUN git clone https://github.com/frost917/customer-manager.git /customer-manager

FROM python:3.8-slim-buster AS run

ENV LC_CTYPE=ko_KR.UTF-8 \
    LC_TIME=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8

COPY --from=clone /customer-manager /customer-manager

WORKDIR /customer-manager/backend/

RUN pip install --no-cache-dir -r /customer-manager/backend/requirements.txt

WORKDIR /customer-manager/backend/src/

CMD python main.py

EXPOSE 443
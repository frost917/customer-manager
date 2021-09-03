FROM python:3.8-slim-buster

ENV LC_ALL=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8

RUN apt update && apt install -y git locales \
    && locale-gen \
    && dpkg-reconfigure locales

WORKDIR /customer-manager
VOLUME [ "/customer-manager" ]

RUN git clone https://github.com/frost917/customer-manager.git /customer-manager \
    && git checkout dev

RUN pip install --no-cache-dir -r requirements.txt

CMD tail -f /dev/null
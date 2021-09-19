FROM alpine/git AS clone

RUN git clone https://github.com/frost917/customer-manager.git /customer-manager \
    && git checkout frontend

FROM python:3.8-slim-buster AS RUN

ENV LC_CTYPE=ko_KR.UTF-8 \
    LC_TIME=ko_KR.UTF-8 \
    LANG=ko_KR.UTF-8 \
    LANGUAGE=ko_KR.UTF-8

RUN apt update && apt install -y locales \
    && locale-gen \
    && dpkg-reconfigure locales

COPY --from=clone /customer-manager /customer-manager

WORKDIR /customer-manager

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /customer-manager/frontend/src/

CMD python main.py
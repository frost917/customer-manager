FROM alpine/git AS source

WORKDIR /

RUN git clone https://github.com/frost917/customer-manager.git

FROM python:3.9.5-slim-buster AS python

COPY --from=source /customer-manager /
WORKDIR /customer-manager

RUN pip install --no-cache-dir -r src/requirements.txt

CMD tail -f /dev/null
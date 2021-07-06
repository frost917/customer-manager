FROM python:3.9.5-slim-buster

RUN apt update && apt install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && git clone https://github.com/frost917/customer-manager.git src\
    && pip install --no-cache-dir -r /src/requirements.txt
    # && pip install --no-cache-dir flask psycopg2-binary
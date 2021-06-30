FROM python:3.9.5-slim-buster
COPY src /src
RUN cd /src \
#    && pip install --no-cache-dir -r /src/requirements.txt
    && pip install --no-cache-dir flask psycopg2-binary
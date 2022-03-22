FROM python:3.8-alpine

WORKDIR /app

ENV TZ Europe/Moscow

RUN apk add --no-cache tzdata && \
    apk update && \
    apk add --no-cache --virtual .build-deps gcc musl-dev && \
    apk add zlib-dev jpeg-dev gcc musl-dev && \
    apk add --no-cache g++ freetype-dev jpeg-dev && \
    apk add --no-cache libpq-dev gcc

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --ignore-installed

COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT /app/entrypoint.sh

COPY docker/.env /app/backend/.env
COPY . /app/backend/
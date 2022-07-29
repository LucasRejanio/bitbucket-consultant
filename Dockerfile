FROM python:3.10.5-alpine3.16

ARG USER_ID=1000

COPY requirements.txt .

RUN adduser -u ${USER_ID} -h /app -D will \
    && pip install -r requirements.txt

COPY --chown=will:will src /app
WORKDIR /app
USER will
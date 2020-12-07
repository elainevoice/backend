FROM python:3.8-slim as base

FROM base as builder
RUN mkdir /install
WORKDIR /install

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
    && apt-get -y --no-install-recommends install build-essential \
    && pip install --no-cache --prefix=/install --no-warn-script-location -r /tmp/requirements.txt

FROM base

COPY --from=builder /install /usr/local


COPY ./docker_scripts/gunicorn_conf.py /gunicorn_conf.py

COPY ./docker_scripts/start-reload.sh /start-reload.sh

RUN chmod +x /start-reload.sh


RUN apt-get update \
    && apt-get install -y libportaudio2 libsndfile-dev espeak libzbar-dev ffmpeg

RUN mkdir -p /app/

ENV PYTHONPATH=/app

EXPOSE 80

CMD ["/start-reload.sh"]

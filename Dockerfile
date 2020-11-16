
FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN apt-get update \
    && apt-get install -y libportaudio2 libsndfile-dev espeak build-essential libzbar-dev 

ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /app/

WORKDIR /app/

ADD api ./api/
ADD assets/ ./assets/
ADD main.py ./main.py

CMD "/start-reload.sh"
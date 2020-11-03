FROM tiangolo/uvicorn-gunicorn:python3.7

RUN apt-get update \
    && apt-get install -y libportaudio2 libsndfile-dev 

ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /app/

WORKDIR /app/

ADD api ./api/
ADD assets/ ./assets/
ADD main.py ./main.py

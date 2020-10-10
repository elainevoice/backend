FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

RUN apt-get update \
    && apt-get install -y libportaudio2 libsndfile-dev 

ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

ADD api ./api/
ADD assets/ ./assets/
ADD main.py ./main.py
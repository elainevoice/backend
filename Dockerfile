
FROM tiangolo/uvicorn-gunicorn:python3.8-slim

RUN apt-get update \
    && apt-get install -y libportaudio2 libsndfile-dev espeak build-essential libzbar-dev 

RUN apt-get install -y ffmpeg

ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

# RUN apt-get install -y python-pip python-dev build-essential
# RUN pip install torch==1.2.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN mkdir -p /app/

WORKDIR /app/

ADD api ./api/
ADD assets/ ./assets/
ADD main.py ./main.py

CMD "/start-reload.sh"
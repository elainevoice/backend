# set base image of the build stage
FROM tiangolo/uvicorn-gunicorn:python3.8-slim AS build_stage

# add the dependencies file to a temporary directory
ADD requirements.txt /tmp/

# update and install essential packages
RUN apt-get update \
    && apt-get install -y \
    build-essential

# install the dependencies to the local user directory (eg. /root/.local)
RUN pip install --user -r /tmp/requirements.txt

# Linux - Cuda only
# remove comments when necessary
# RUN apt-get install -y python-pip python-dev build-essential
# RUN pip install torch==1.2.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# set base image of the production stage
FROM tiangolo/uvicorn-gunicorn:python3.8-slim AS production_stage

# copy the build stage result to the production stage
COPY --from=build_stage /root/.local /root/.local

# update PATH environment variable
ENV PATH=/root/.local/bin:$PATH

# update and install essential packages
RUN apt-get update \
    && apt-get install -y \
    libportaudio2 \
    libsndfile-dev \
    espeak \
    build-essential \
    libzbar-dev 

# install ffmpeg
RUN apt-get install -y ffmpeg

# Avoid possible error
RUN pip install ffmpeg-python ffmpeg

# create the app directory
RUN mkdir -p /app/

# set the work directory to the newly created directory.
WORKDIR /app/

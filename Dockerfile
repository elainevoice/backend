FROM python:3-alpine

RUN python -m pip install --upgrade pip
RUN set -e; \
        apk add --no-cache --virtual .build-deps \
                gcc \
                libc-dev \
                linux-headers \
        ;

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt 

COPY . /tmp/

WORKDIR /tmp/

CMD ["python","/tmp/src/api.py"]

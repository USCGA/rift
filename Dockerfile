#FROM python:alpine3.11
FROM alpine

LABEL maintainer="richard@richardbew.com"

EXPOSE 8000

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN apk update

RUN apk add python3 py3-pip

RUN apk add --no-cache --virtual .build-deps gcc libffi-dev musl-dev python3-dev py3-wheel \
     && python3 -m pip install -r requirements.txt \
     && apk del .build-deps gcc libffi-dev musl-dev python3-dev py3-wheel

#RUN apk update
# Build tools
#RUN apk add --no-cache --virtual build-base python3-dev libffi-dev
# Python
#RUN apk add python3 py3-pip

#RUN python3 -m pip install -r requirements.txt

COPY ./rift /app/rift
COPY ./run.py /app

CMD [ "source", "venv/bin/activate" ]
CMD [ "gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "run:app" ]

FROM python:3.7

ENV APP_ROOT /test_task
RUN mkdir /test_task

RUN apt-get update

WORKDIR ${APP_ROOT}

COPY requirements.txt ${APP_ROOT}/
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED 1
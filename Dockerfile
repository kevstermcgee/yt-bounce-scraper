FROM ubuntu:latest
LABEL authors="TheNa"

FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

COPY . .

CMD [ "python", "main.py" ]

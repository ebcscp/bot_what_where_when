FROM python:3.9-alpine

RUN adduser -D worker	
WORKDIR /home/worker

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY worker worker/
COPY config.yml .
COPY main.py .

USER worker
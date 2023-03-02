FROM python:3.9-alpine

RUN adduser -D poller	
WORKDIR /home/poller

#CMD ["export", "PYTHONPATH", "=", "."]
ENV PYTHONPATH "${PYTHONPATH}:/home"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY poller poller
COPY rabbit rabbit
COPY __init__.py .
COPY config.yml .
COPY dataclass_config.py .
COPY main.py .

USER poller


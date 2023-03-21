FROM python:3.9-alpine

RUN adduser -D bot	
WORKDIR /home/bot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY admin admin/
COPY alembic alembic/
COPY database database/
COPY alembic.ini main.py app.py config.yml logger.py manager.py tg_api.py set_config.py  ./

COPY worker worker/
COPY config.yml .

USER bot

FROM python:3.9-alpine

RUN adduser -D bot	

WORKDIR /home/bot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY admin admin/
COPY alembic alembic/
COPY bot bot/
COPY database database/
COPY game game/
COPY alembic.ini config.yml dataclass_config.py dataclasses_models.py main_config.py main.py store.py tg_api.py worker.py ./

USER bot

SHELL  ["bin/bash", "-c", "python -m alembic revision --autogenerate -m 'Add init table'"]
# SHELL ["/bin/bash", "-c", "python -m alembic upgrade head"]
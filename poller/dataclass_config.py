
from dataclasses import dataclass


@dataclass
class RabbitConfig:
    queue_name: str
    exchange_name: str
    rabbit_url: str


@dataclass
class TgConfig:
    token: str
    api_path: str



@dataclass
class Config:
    rabbit: RabbitConfig = None
    tg: TgConfig = None
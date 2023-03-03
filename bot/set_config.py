
import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app import Application


@dataclass
class SessionConfig:
    key: str


#@dataclass
#class AdminConfig:
    #email: str
    #password: str


@dataclass
class BotConfig:
    token: str
    group_id: int
    v: str


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "admin"
    password: str = "1111Aa"
    database: str = "kurs"


@dataclass
class Config:
    session: SessionConfig = None
    bot: BotConfig = None
    database: DatabaseConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        bot=BotConfig(
            token=raw_config["bot"]["token"],
            group_id=raw_config["bot"]["group_id"],
            v=raw_config["bot"]["v"],
        ),
        database=DatabaseConfig(**raw_config["database"]),
    )
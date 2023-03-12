from dataclass_config import BaseConfig, WorkerConfig, Config,  TgConfig, Game 
import typing
if typing.TYPE_CHECKING:
    from worker import Worker
import yaml

def worker_config(bot:"Worker",config_path: str) -> Config:
    with open(config_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)
    bot.config = Config(
        worker_config=WorkerConfig(
            rabbit_url=raw_config["rabbitmq"]["rabbit_url"],
            queue_name=raw_config["rabbitmq"]["queue_name"],
            bot_id=raw_config["bot"]["id"],            
        ),
        base_config=BaseConfig(
            base_url=raw_config["database"]["base_url"],
        ),
        tg_config=TgConfig(
            token=raw_config["bot"]["token"],
            api_path=raw_config["bot"]["api_path"], 
        ),
        game=Game(
            user=raw_config["game"]["user"],
            questions=raw_config["game"]["questions"], 
        ),
    )    
     




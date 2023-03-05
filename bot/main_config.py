from dataclass_config import BaseConfig, WorkerConfig, Config
import yaml

def worker_config(config_path: str) -> Config:
    with open(config_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)
    return Config(
        Worker_config=WorkerConfig(
            rabbit_url=raw_config["rabbitmq"]["rabbit_url"],
            queue_name=raw_config["rabbitmq"]["queue_name"],   
            token=raw_config["bot"]["token"],
            api_path=raw_config["bot"]["api_path"],           
        ),
        Base_config=BaseConfig(
            base_url=raw_config["database"]["base_url"],
        )  
    )    
     




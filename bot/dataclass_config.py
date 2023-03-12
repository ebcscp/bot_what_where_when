from dataclasses import dataclass


@dataclass
class WorkerConfig:
    rabbit_url: str
    queue_name: str
    bot_id: int


@dataclass
class BaseConfig:
    base_url:str

@dataclass
class TgConfig:
    token: str
    api_path: str

@dataclass
class Game:
    user: str
    questions: str
    
@dataclass
class Config:
    worker_config: WorkerConfig = None
    base_config: BaseConfig = None 
    tg_config: TgConfig = None 
    game: Game = None  
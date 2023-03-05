from dataclasses import dataclass


@dataclass
class WorkerConfig:
    rabbit_url: str
    queue_name: str
    token: str
    api_path: str

@dataclass
class BaseConfig:
    base_url:str

@dataclass
class Config:
    Worker_config: WorkerConfig = None
    Base_config: BaseConfig = None    
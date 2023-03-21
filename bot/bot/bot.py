from worker import Worker
from main_config import worker_config
from store import setup_store

bot = Worker()      

def setup_config(config_path:str):
    worker_config(bot, config_path)
    setup_store(bot)
    return bot
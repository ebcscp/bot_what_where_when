import os
from worker import run_worker
from bot.bot import setup_config

if __name__ == "__main__":
    run_worker(
        setup_config(
            config_path=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "config.yml"            
            )
        )
    )

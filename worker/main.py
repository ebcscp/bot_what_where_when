import os
from worker.worker import run_worker

if __name__ == "__main__":
    run_worker(
            config_path=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "config.yml"            
        )
    )
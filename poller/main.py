import os
from poller.poller.poller import run_poller, setup_config

if __name__ == "__main__":
    run_poller(
        setup_config(
            config_path=os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "config.yml"
            )
        )
    )
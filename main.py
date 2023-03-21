from app.app import setup_app
from aiohttp.web import  run_app


if __name__ == '__main__':
    run_app(setup_app('config.yml'), port=9090)
from dataclasses import dataclass
import asyncio
from aio_pika import connect, Message
from models import UpdateObj
import aio_pika
import json
import yaml
from tg_api import TgClient
from manager import TgApiAccessor
from database.database import Database
from database.base_accessor import Database
from main_config import worker_config
from store import setup_store
from dataclass_config import BaseConfig,Config,WorkerConfig

@dataclass
class WorkerConfig:
    rabbit_url: str
    queue_name: str
    base_url:str
    token: str
    api_path: str

class Worker:
    def __init__(self, config: Config):
        self.workerconfig = config.Worker_config
        self.baseconfig = config.Base_config
        self.conect_work = False
        self.connection = None
        self.consume_q = None
        self.count_worker = 0
        self.stop_event = asyncio.Event()
        self.tg_client = TgClient(self.workerconfig.token, self.workerconfig.api_path) 
        self.queue = None
        self.tg_api_accessor = TgApiAccessor()
        self.pgcli = Database()

    async def handler(self, msg: aio_pika.IncomingMessage):

        upd = UpdateObj.Schema().loads(msg.body)
        # print(f'ТЕСТ  {upd}  ТЕСТ')
        if upd.message.document:
            file = await self.tg_client.get_file(upd.message.document.file_id)
            url = f'{self.workerconfig.api_path}/file/bot{self.workerconfig.token}/{file.file_path}'
            await self.tg_api_accessor._get_admin_worker(upd.message.chat.id, url)

        # await self.tg_client.send_message(upd.message.chat.id, massege) 
        
            
    async def _worker(self, msg: aio_pika.IncomingMessage):

        async with msg.process():
            self.count_worker += 1
            try:
                await self.handler(msg)
            finally:
                self.count_worker -= 1
                if not self.is_runnig and self.conect_work == 0:
                    self.stop_event.set()
  

    async def _setup(self):
        if self.conect_work:
            return
        self.connection = await connect(url= self.workerconfig.rabbit_url)
        self.channel = await self.connection.channel()
        #await self.channel.set_qos(prefetch_count=self.config.capacity)
        self.queue = await self.channel.declare_queue(self.workerconfig.queue_name)
        
        self.conect_work = True


    async def start(self):
        await self._setup()   
        await self.database.connect(self.baseconfig.base_url)   
        self.is_runnig = True       
        self.consume_q = await self.queue.consume(self._worker)

    
    async def stop(self):
        if self.consume_q:
            await self.queue.cancel(self.consume_q)
        self.is_runnig = False  
        if self.count_worker !=0:
            self.stop_event = asyncio.Event()
            await self.stop_event.wait()
        if self.connection:
            await self.connection.close()
        await self.database.disconnect()  
        
def setup_config(config_path:str):
    bot = Worker(worker_config(config_path=config_path))  
    setup_store(bot)
    return bot


def run_worker(bot:str):

    # with open(config_path, "r", encoding="utf-8") as f:
    #         raw_config = yaml.safe_load(f)

    # Worker_config=WorkerConfig(
    #         rabbit_url=raw_config["rabbitmq"]["rabbit_url"],
    #         queue_name=raw_config["rabbitmq"]["queue_name"], 
    #         base_url=raw_config["database"]["base_url"],  
    #         token=raw_config["bot"]["token"],
    #         api_path=raw_config["bot"]["api_path"],           
    #     )
    
    # worker = Worker(Worker_config)

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.stop())

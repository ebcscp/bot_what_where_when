from dataclasses import dataclass
import asyncio
from aio_pika import connect, Message
from worker.models import UpdateObj
import aio_pika
import json
import yaml
from worker.tg_api import TgClient



@dataclass
class WorkerConfig:
    rabbit_url: str
    queue_name: str


class Worker:
    def __init__(self, config: WorkerConfig):
        self.config = config
        self.conect_work = False
        self.connection = None
        self.consume_q = None
        self.count_worker = 0
        self.stop_event = asyncio.Event()
        self.tg_client = TgClient()
        self.queue = None

    async def handler(self, msg: aio_pika.IncomingMessage):

        upd = UpdateObj.Schema().loads(msg.body)
        await self.tg_client.send_message(upd.message.chat.id, '[nice to meet you]') 
        print(f'ТЕСТ  {upd}  ТЕСТ')
        #await self.handle_update(upd)
            
    async def _worker(self, msg: aio_pika.IncomingMessage):

        async with msg.process():
            self.count_worker += 1
            try:
                await self.handler(msg)
            finally:
                self.count_worker -= 1
                if not self.is_runnig and self.conect_work == 0:
                    self.stop_event.set()


        #raise NotImplementedError     

    async def _setup(self):
        if self.conect_work:
            return
        self.connection = await connect(url= self.config.rabbit_url)
        self.channel = await self.connection.channel()
        #await self.channel.set_qos(prefetch_count=self.config.capacity)
        self.queue = await self.channel.declare_queue(self.config.queue_name)
        self.conect_work = True

    async def start(self):
        """
        объявить очередь и добавить обработчик к ней
        """
        await self._setup()
        self.is_runnig = True
        self.consume_q = await self.queue.consume(self._worker)
  
          

    async def stop(self):
        """
        закрыть все ресурсы, с помощью которых работали с rabbit
        """
        if self.consume_q:
            await self.queue.cancel(self.consume_q)
        self.is_runnig = False  
        if self.count_worker !=0:
            self.stop_event = asyncio.Event()
            await self.stop_event.wait()
        if self.connection:
            await self.connection.close()

def run_worker(config_path:str):

    with open(config_path, "r", encoding="utf-8") as f:
            raw_config = yaml.safe_load(f)

    Worker_config=WorkerConfig(
            rabbit_url=raw_config["rabbitmq"]["rabbit_url"],
            queue_name=raw_config["rabbitmq"]["queue_name"],            
        )
    
    worker = Worker(Worker_config)

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(worker.start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(worker.stop())

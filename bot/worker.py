from dataclasses import dataclass
import asyncio
from aio_pika import connect, Message
from models import UpdateObj
import aio_pika

class Worker:
    def __init__(self):
        self.config = None
        self.conect_work = False
        self.connection = None
        self.consume_q = None
        self.count_worker = 0
        self.stop_event = asyncio.Event()
        self.tg_client = None
        self.queue = None
        self.pgcli = None
        self.store = None

    async def handler(self, msg: aio_pika.IncomingMessage):
        upd = UpdateObj.Schema().loads(msg.body)
        print(f'ТЕСТ  {upd.my_chat_member}  ТЕСТ')
        if upd.message.document:
            file = await self.store.tg_client.get_file(upd.message.document.file_id)
            file = await self.store.tg_client.get_file(upd.message.document.file_id)
            url = f'{self.config.tg_config.api_path}/file/bot{self.config.tg_config.token}/{file.file_path}'
            await self.store.manager._get_admin_worker(upd.message.chat.id, url)
        #elif upd.message.
        #await self.store.tg_client.send_message(upd.message.chat.id, upd.message.text) 
        
            
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
        self.connection = await connect(url= self.config.worker_config.rabbit_url)
        self.channel = await self.connection.channel()
        #await self.channel.set_qos(prefetch_count=self.config.capacity)
        self.queue = await self.channel.declare_queue(self.config.worker_config.queue_name)
        
        self.conect_work = True


    async def start(self):
        await self._setup()   
        await self.pgcli.connect(self.config.base_config.base_url)   
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
        await self.pgcli.disconnect()  


def run_worker(bot:str):
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.stop())
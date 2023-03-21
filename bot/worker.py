from dataclasses import dataclass
import asyncio
from aio_pika import connect, Message
from dataclasses_models import UpdateObj
import aio_pika

from bot.enum_blanks import Commands, CallBackData

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
        #print(msg.body)
        upd = UpdateObj.Schema().loads(msg.body)
        print(upd)
        if upd.message:
            if upd.message.text == Commands.Start.value:
                await self.store.manager.start_game(upd)
            elif upd.message.text == Commands.Stop.value:
                await self.store.manager.bot_stop_game(upd)
                      
            elif upd.message.document and upd.message.chat.id == self.config.worker_config.chat_id:
                file = await self.store.tg_client.get_file(upd.message.document.file_id)
                file = await self.store.tg_client.get_file(upd.message.document.file_id)
                url = f'{self.config.tg_config.api_path}/file/bot{self.config.tg_config.token}/{file.file_path}'
                await self.store.manager._get_admin_worker(url) 
            else:
                await self.store.manager.begin_game(upd)     
        elif upd.my_chat_member and upd.my_chat_member.new_chat_member.user.id == self.config.worker_config.bot_id:
            await self.store.manager.add_bot_chat(upd)
        elif (upd.callback_query and upd.callback_query.data == Commands.Start.value):
            await self.store.manager.start_game(upd)
        elif (upd.callback_query and upd.callback_query.data == Commands.Stop.value):
            await self.store.manager.bot_stop_game(upd)        
        elif upd.callback_query and upd.callback_query.data == CallBackData.IJoin.value:
            await self.store.manager.join_user_game(upd=upd)
        elif upd.callback_query and upd.callback_query.data == CallBackData.WeReady.value:
            await self.store.manager.ready_game(upd=upd)
        elif upd.callback_query and upd.callback_query.data == CallBackData.Go.value:
            await self.store.manager.begin_game(upd=upd)
        elif upd.callback_query and upd.callback_query.data == CallBackData.Erly.value:
            await self.store.manager.erly_response(upd=upd)             
        elif upd.my_chat_member: #для кнопок с пользаками
             await self.store.manager.begin_game(upd)  
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
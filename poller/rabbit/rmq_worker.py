from dataclasses import dataclass
import asyncio
from aio_pika import connect, Message
import aio_pika
import json

@dataclass
class WorkerConfig:
    rabbit_url: str
    queue_name: str
    token:str
    
class WorkerRmq:
    def __init__(self, config: WorkerConfig):
        self.config = config
        self.conect_work = False
        self.connection = None
        
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def _setup(self):
        if self.conect_work:
            return   
        self.connection = await connect(url= self.config.rabbit_url)
        self.channel = await self.connection.channel()
        await self.channel.declare_queue(self.config.queue_name)
        self.conect_work = True

    async def put(self, data: dict):

        await self._setup()
        await self.channel.default_exchange.publish(
            Message(
            json.dumps(data).encode()),
            routing_key=self.config.queue_name,
            )

    async def stop(self):

        if self.connection:
            await self.connection.close()
import asyncio
from typing import Optional
from poller import Client, poller_config
from poller.poller.models import UpdateObj



class Poller:
    def __init__(self, client: Client):
        self.tg_client = client.tg_cli
        self.rabbit_client = client.rabbit_cli
        self.is_running = True
        self._task: Optional[asyncio.Task] = None

    async def poll(self):
        
        offset = 0
        while self.is_running:
            try:
                updates = await self.tg_client.get_updates_in_objects(offset=offset, timeout=60)
                
                for update in updates:
                    print(update)
                    offset = update.update_id + 1
                    data = UpdateObj.Schema().dump(update)
                    await self.rabbit_client.put(data)
            except Exception as e:
                update = await self.tg_client.get_updates(offset=offset, timeout=5)
                


    async def start(self):
        
        self.is_running = True
        self._task = asyncio.create_task(self.poll())

    async def stop(self):

        self.is_running = False
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass

        await self.rabbit_client.stop()        

def setup_config(config_path:str):
    config =  poller_config(config_path=config_path)  
    clients = Client(config)    
    poller = Poller(clients)
    return poller

def run_poller(poller:Poller):

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(poller.start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(poller.stop())
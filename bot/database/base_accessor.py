from logging import getLogger
from sqlalchemy.engine import ChunkedIteratorResult
from database.database import Database

class BaseAccessor(Database):
    def __init__(self, *args, **kwargs):
        self.logger = getLogger("accessor")
        #self.session = 

    async def select(self, query):
        async with self.session() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            return res
        
    async def insert(self, new_obj):
        print(self.session)
        async with self.session() as session:   
             async with session.begin():
                print(1)
                session.add(new_obj)
                await session.commit() 
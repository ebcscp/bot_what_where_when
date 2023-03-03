import typing
from logging import getLogger
from sqlalchemy.engine import ChunkedIteratorResult
from database.database import Database

class BaseAccessor:
    def __init__(self, *args, **kwargs):
        self.logger = getLogger("accessor")
        self.database = Database()

    async def select(self, query):
        async with self.database.session() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            return res
        
    async def insert(self, new_obj):
        async with self.database.session() as session:
             async with session.begin():
                session.add(new_obj)
                await session.commit() 
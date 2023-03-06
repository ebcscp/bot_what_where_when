import typing
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import ChunkedIteratorResult

from sqlalchemy.ext.asyncio import create_async_engine
from database.sqlalchemy_base import db


if typing.TYPE_CHECKING:
    from worker import Worker


class Database:
    def __init__(self, bot: "Worker"):
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None
        self.bot = bot


    async def connect(self, base_url, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(base_url, echo=True, future=True)
        self.session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)  

        
    async def disconnect(self, *_: list, **__: dict) -> None:
        if self.session:
            await self.session().close()
        if self._engine:
            await self._engine.dispose() 
            

    async def select(self, query):
        async with self.session() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            return res
        
        
    async def insert(self, new_obj):
        print(self.bot.pgcli.session())
        async with self.session() as session:   
             async with session.begin():
                print(1)
                session.add(new_obj)
                await session.commit()   
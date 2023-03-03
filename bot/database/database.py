
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_base import db



class Database:
    def __init__(self):
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None


    async def connect(self, base_url, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(base_url, echo=True, future=True)
        self.session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)       
        
    async def disconnect(self, *_: list, **__: dict) -> None:
        if self.session:
            await self.session().close()
        if self._engine:
            await self._engine.dispose()    
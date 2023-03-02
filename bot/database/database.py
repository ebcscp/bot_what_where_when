
from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine
from database.sqlalchemy_base import db


if TYPE_CHECKING:
    from app.web.app import Application

BASE_URL = "postgresql+asyncpg://kts_user:kts_pass@localhost/kts"

class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None


    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(BASE_URL, echo=True, future=True)
        self.session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)       
        
    async def disconnect(self, *_: list, **__: dict) -> None:
        if self.session:
            await self.session().close()
        if self._engine:
            await self._engine.dispose()    
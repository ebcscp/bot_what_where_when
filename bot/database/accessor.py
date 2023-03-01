import typing
from logging import getLogger
from sqlalchemy.engine import ChunkedIteratorResult

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BaseAccessor:
    def __init__(self, app: "Application", *args, **kwargs):
        self.app = app
        self.logger = getLogger("accessor")
        app.on_startup.append(self.connect)
        app.on_cleanup.append(self.disconnect)

    async def connect(self, app: "Application"):
        return

    async def disconnect(self, app: "Application"):
        return

    async def select(self, query):
        async with self.app.database.session() as session:
            res: ChunkedIteratorResult = await session.execute(query)
            return res
        
    async def insert(self, new_obj):
        async with self.app.database.session() as session:
             async with session.begin():
                session.add(new_obj)
                await session.commit() 
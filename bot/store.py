import typing
from database.database import Database


if typing.TYPE_CHECKING:
    from worker import Worker


class Store:
    def __init__(self, bot: "Worker"):

        from admin.accessor import AdminAccessor
        from manager import TgApiAccessor
        from tg_api import TgClient

        self.admins = AdminAccessor(bot)
        self.manager = TgApiAccessor(bot)
        self.tg_client = TgClient(bot)

def setup_store(bot: "Worker"):
    bot.pgcli = Database(bot)
    #bot.tg_client = TgClient(bot)
    bot.store = Store(bot)



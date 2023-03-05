import typing
from database.database import Database


if typing.TYPE_CHECKING:
    from worker import Worker


class Store:
    def __init__(self, bot: "Worker"):

        from admin.accessor import AdminAccessor

        self.admins = AdminAccessor(bot)



def setup_store(bot: "Worker"):
    bot.pgcli = Database(bot)



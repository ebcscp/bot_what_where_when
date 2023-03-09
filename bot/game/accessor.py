from database.database import Database
from game.models import Session, SessionsModel, StateEnum, SessionUsersModel, UsersModel, User 
from sqlalchemy import select, update, and_, not_

class GameAccessor(Database):

    async def get_gs_in_chat(self, chat_id: int, lst_state: list[StateEnum]) -> SessionsModel:
        query = self.select(SessionsModel).where(
            and_(
                SessionsModel.chat_id == chat_id,
                SessionsModel.state.in_(lst_state),
            )
        )
        gs = (await self.bot.pgcli.select(query)).scalars().first()
        return gs

    async def check_user_session(self, id):
        query = self.select(UsersModel).where(SessionsModel.tg_id == id)
        raw_query = query.first()
        return raw_query

    async def creat_user_session(self, id, first_name, username):
        result = await self.check_user_session()
        if result:
            return result
        else:
            user_model = User(tg_id=id, first_name=first_name, username=username)
            self.insert(user_model)    
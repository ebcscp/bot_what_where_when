from database.database import Database
from game.models import Session, SessionsModel, StateEnum, SessionUsersModel, UsersModel, QuestionModel, AnswerModel, SessionQuestionModel , RoundsModel
from sqlalchemy import select as alselsect, update, and_, not_ , func
from sqlalchemy.orm import joinedload


class GameAccessor(Database):

    async def get_session_in_chat(self, chat_id: int, lst_state ) -> SessionsModel:
        query = alselsect(SessionsModel).where(
            and_(
                SessionsModel.id_chat == chat_id,
                SessionsModel.status.in_(lst_state),
            )
        )
        gs = (await self.bot.pgcli.select(query)).scalars().first()
        return gs

    async def check_user(self, id):
        #query = await alselsect(UsersModel).where(UsersModel.tg_id == id).scalars().first()
        query = alselsect(UsersModel).where(UsersModel.tg_id == id)
        result = (await self.bot.pgcli.select(query)).scalars().first()
        
        return result
    
    async def check_user_id(self, id):
        #query = await alselsect(UsersModel).where(UsersModel.tg_id == id).scalars().first()
        query = alselsect(UsersModel).where(UsersModel.id == id)
        result = (await self.bot.pgcli.select(query)).scalars().first()
        
        return result
    
    async def creator_is_ready(self, id_, ready_to_play:bool):

        update_query = update(SessionUsersModel).where(SessionUsersModel.id == id_).values(ready_to_play=ready_to_play)
        result = await self.bot.pgcli.update(update_query)
        return result
 

    
    async def creat_user(self, tg_id,  first_name, username):
        result = await self.check_user(tg_id)
        if result:
            return result
        else:
            user_model = UsersModel(tg_id=tg_id, first_name=first_name, username=username)
            await self.bot.pgcli.insert(user_model) 
            return user_model
        
        
    async def create_session(self, start_date, id_chat, status):
        session_model = SessionsModel(start_date=start_date, id_chat=id_chat, status=status)
        await self.bot.pgcli.insert(session_model) 
        return session_model
    
    
    async def create_user_session(self, sessions_id, users_id, is_creator =False, is_captain = False, ready_to_play = False):
        session_model = SessionUsersModel(sessions_id=sessions_id, users_id=users_id, is_creator=is_creator, is_captain=is_captain, ready_to_play=ready_to_play)
        await self.bot.pgcli.insert(session_model) 
        return session_model
    
    
    async def check_user_session(self, id_, id_session):
        query = alselsect(SessionUsersModel).join(UsersModel).where(
            and_(
                UsersModel.tg_id == id_,
                SessionUsersModel.sessions_id == id_session
                )
        ).options(joinedload(SessionUsersModel.users).options(joinedload(UsersModel.user_sessions)))
        result = (await self.bot.pgcli.select(query)).scalars().first()
        return result
    
    async def check_all_user_session(self, session_id):
        query = alselsect(SessionUsersModel).where(SessionUsersModel.sessions_id == session_id) \
            .options(joinedload(SessionUsersModel.users).options(joinedload(UsersModel.user_sessions)))
        result = await self.bot.pgcli.select(query)
        return  [us.users for us in result.scalars().unique()]
    
    
    async def check_user_session_reade_to_play(self, session_id, ready_to_play):
        query = alselsect(SessionUsersModel).where(
            and_(
                SessionUsersModel.sessions_id == session_id,
                SessionUsersModel.ready_to_play == ready_to_play
                )
            )
        
        result = (await self.bot.pgcli.select(query)).scalars().first()
        return result
    
    async def check_user_session_captain(self, chat_id):
        query = alselsect(SessionUsersModel).join(SessionsModel).where(
            and_(
                SessionUsersModel.is_captain == True,
                SessionsModel.id_chat == chat_id
            )).options(joinedload(SessionUsersModel.users).options(joinedload(UsersModel.user_sessions))) \
            .options(joinedload(SessionUsersModel.sessions).options(joinedload(SessionsModel.user_sessions)))

        us = (await self.bot.pgcli.select(query)).scalars().first()
        return us

    async def check_user_session_id_captain(self, chat_id, session_id):
        query = alselsect(SessionUsersModel).join(SessionsModel).where(
            and_(
                SessionUsersModel.is_captain == True,
                SessionsModel.id_chat == chat_id,
                SessionsModel.id == session_id
            )).options(joinedload(SessionUsersModel.users).options(joinedload(UsersModel.user_sessions))) \
            .options(joinedload(SessionUsersModel.sessions).options(joinedload(SessionsModel.user_sessions)))

        us = (await self.bot.pgcli.select(query)).scalars().first()
        return us
    
    async def update_status_session(self, id_, status ):
        update_query = update(SessionsModel).where(SessionsModel.id == id_).values(status=status)
        result = await self.bot.pgcli.update(update_query)
        return result
    
    
    async def update_status_session_end(self,id_, status, end_date, result):
        update_query = update(SessionsModel).where(SessionsModel.id == id_).values(status=status, end_date= end_date, result=result)
        resultt = await self.bot.pgcli.update(update_query)
        return resultt
    
    
    async def check_session(self, id_, status):
        query = alselsect(SessionsModel).where(
            and_(
                    SessionsModel.id == id_,
                    SessionsModel.status == status,
                ) )
        result = (await self.bot.pgcli.select(query)).scalars().first()
        return result
    
    async def check_session_chat_id(self, chat_id, status):
        query = alselsect(SessionsModel).where(
            and_(
                    SessionsModel.id_chat == chat_id,
                    SessionsModel.status == status,
                ) 
            )
        result = (await self.bot.pgcli.select(query)).scalars().first()
       
        return result
    

    
    async def check_sesion_status(self, id_):
        query = alselsect(SessionsModel).where(SessionsModel.id == id_)
        result = (await self.bot.pgcli.select(query)).scalars().first()
       
        return result
    
    
    async def check_master_session(self, chat_id, session_id):
        query = alselsect(SessionUsersModel).join(SessionsModel).where(
            and_(
                SessionUsersModel.is_creator == True,
                SessionsModel.id_chat == chat_id,
                SessionUsersModel.sessions_id == session_id
            )).options(joinedload(SessionUsersModel.users).options(joinedload(UsersModel.user_sessions))) \
            .options(joinedload(SessionUsersModel.sessions).options(joinedload(SessionsModel.user_sessions)))

        us = (await self.bot.pgcli.select(query)).scalars().first()
        return us
    
    async def rand_user_is_captain(self, sessionsid: int):
        query = alselsect(SessionUsersModel).where(SessionUsersModel.sessions_id == sessionsid) \
            .options(joinedload(SessionUsersModel.users).options(joinedload(UsersModel.user_sessions))) \
            .options(joinedload(SessionUsersModel.sessions).options(joinedload(SessionsModel.user_sessions))) \
            .order_by(func.random()).limit(1)

        result = (await self.bot.pgcli.select(query)).scalars().first()
        update_query = update(SessionUsersModel).where(SessionUsersModel.id == result.id).values(is_captain = True)
        await self.bot.pgcli.update(update_query)
        return result
    
    async def rand_questions_for_sessions(self, limit, session_id):
        query = alselsect(QuestionModel).order_by(func.random()).limit(limit)

        result = await self.bot.pgcli.select(query)
        us = [us.id for us in result.scalars().unique()]
        for id in us:
            query = SessionQuestionModel(id_qusetion=id, id_session=session_id, is_answerd=False)
            await self.bot.pgcli.insert(query) 
        return us    
    
    async def get_session_question_for_chat(self):
        query = alselsect(SessionQuestionModel).join(QuestionModel).where(SessionQuestionModel.is_answerd == False)\
            .options(joinedload(SessionQuestionModel.question).options(joinedload(QuestionModel.session_question))) \
            .options(joinedload(SessionQuestionModel.sessions).options(joinedload(SessionsModel.session_question))) \
            .order_by().limit(1)
        result = (await self.bot.pgcli.select(query)).scalars().first()
        return result
    
    
    async def update_session_question_for_chat(self, id_):
        update_query = update(SessionQuestionModel).where(SessionQuestionModel.id_qusetion == id_).values(is_answerd=True)
        result = await self.bot.pgcli.update(update_query)
        return result
    
    async def add_round(self, id_session, points_team=0 , points_bot=0, round_number=0, responsible=False ):
        query = RoundsModel(id_session = id_session, points_team=points_team, points_bot=points_bot, round_number=round_number, responsible = responsible)
        await self.bot.pgcli.insert(query)
    
    
    async def get_round(self, id_session):
        query = alselsect(RoundsModel).where(RoundsModel.id_session == id_session).order_by(RoundsModel.id.desc())
        result = (await self.bot.pgcli.select(query)).scalars().first()
        return result


    async def check_round_for_existence(self, session_id):
        query = alselsect(RoundsModel).where(RoundsModel.id_session == session_id)
        result = (await self.bot.pgcli.select(query)).scalars().first()
        return result

    async def update_round_user(self, id_,points_team, round_number):
        query = update(RoundsModel).where(RoundsModel.id == id_).values(
                    points_team=points_team,
                    round_number=round_number,
                    responsible= True
                 
            )
        result = await self.bot.pgcli.update(query)
        print(result)
        return result
    
    async def update_round_bot(self, id_,points_bot, round_number):
        query = update(RoundsModel).where(RoundsModel.id == id_).values(
                    points_bot=points_bot,
                    round_number=round_number,
                    responsible= False
                
            )
        result = await self.bot.pgcli.update(query)
        print(result)
        return result
    
    async def get_answer(self, question_id):
        query = alselsect(AnswerModel).where(AnswerModel.question_id == question_id)
        result = await self.bot.pgcli.select(query)
        return  [us.title for us in result.scalars().unique()]
    
    
    async def get_session_not_in_lst_state(self, chat_id: int, lst_state: list[StateEnum]):
        query = alselsect(SessionsModel).where(
            and_(
                SessionsModel.id_chat == chat_id,
                not_(SessionsModel.status.in_(lst_state)),
            )
        )
        gs = (await self.bot.pgcli.select(query)).scalars().first()
        return gs
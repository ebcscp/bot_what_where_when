from urllib.parse import urljoin
import requests
import json
import typing
from datetime import datetime
from asyncio import sleep
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from database.database import Database
from dataclasses_models import UpdateObj
from bot.enum_blanks import BotMsg, BotButtons, StatusAddBot
from game.models import Answer, Question, StateEnum, ResultEnum
from bot.utils import list_user_session, get_chat_id, get_from_


class BotAccessor(Database):
    def __init__(self, bot: "Worker",  *args, **kwargs):
        self.bot = bot

    async def _get_admin_worker(self, url: str = ' ' ):
        response = requests.get(url)
        data = response.content    
        results = json.loads(data) 
        lst_answers = []
        for result in results: 
            for answer in result["answer"]:              
                lst_answers.append(Answer(title=answer))    
            await self.bot.store.admins.create_question(title=result["title"], answers=lst_answers)
            lst_answers = [] 


    async def send_keyboard(self, chat_id: int, text: str):
        rk_markup = ReplyKeyboardMarkup(BotButtons.Keyboard.value, one_time_keyboard=True, resize_keyboard=True)
        await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                 text=text,
                                                 reply_markup=rk_markup)
    
    async def add_bot_chat(self, upd: UpdateObj):
        status = upd.my_chat_member.new_chat_member.status

        if status == StatusAddBot.Member.value:
            await self.bot.store.tg_client.send_message(upd.my_chat_member.chat.id,
                                                     text=BotMsg.add.value,
                                                     reply_markup=InlineKeyboardMarkup(
                                                         inline_keyboard=[BotButtons.StartBtn.value]))

    async def start_game(self, upd):
        chat_id = upd.callback_query.message.chat.id if upd.callback_query else upd.message.chat.id

        check_game_session = await self.bot.store.game.get_session_in_chat(chat_id, lst_state=[StateEnum.ChoiceOfResponder,
                                                                                        StateEnum.Active,
                                                                                        StateEnum.RypleProcess])

        if check_game_session:
            await self.send_keyboard(chat_id=chat_id, text=BotMsg.GameSessionActive.value)
        else:
            from_ = upd.callback_query.from_ if upd.callback_query else upd.message.from_
           # start_date = datetime.fromtimestamp(upd.callback_query.message.date)
            
            user = await self.bot.store.game.creat_user(from_.id, from_.first_name, from_.username)

            new_session = await self.bot.store.game.create_session(id_chat=chat_id,
                                                                   start_date = datetime.now(),
                                                                   status=StateEnum.Established)
            user_session = await self.bot.store.game.create_user_session(sessions_id=new_session.id,
                                                                   users_id=user.id,
                                                                   is_creator=True) 
            
            
            await self.send_keyboard(chat_id=chat_id,
                                     text=BotMsg.MenuDescription.value)
            # TODO: вывести правила игры + кнопки: "Я участвую" и "Завершить набор"
            await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                               text=f"{BotMsg.GameRulesOne.value+ BotMsg.GameRulesTwo.value} \n\n"
                                                                    f"Создатель игровой сессии: {user.first_name}",
                                                               reply_markup=InlineKeyboardMarkup(
                                                                   inline_keyboard=[BotButtons.JoinBtns.value]))    

            await sleep(60)
            print('Прошло 60 сек')
            await self.close_the_user_sessions(chat_id, new_session.id)
            


    async def close_the_sessions_is_no_active(self, chat_id, sessions_id):
        check_game_session = await self.bot.store.game.get_session_in_chat(chat_id, lst_state=[StateEnum.Established])
        
        if check_game_session:
           await self.bot.store.game.update_status_session(sessions_id, StateEnum.Interrupted)

           await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                               text=f"{BotMsg.SessionEndedNotStart.value}",
                                                               reply_markup=InlineKeyboardMarkup(
                                                                   inline_keyboard=[BotButtons.StartBtn.value]))

    
    async def close_the_user_sessions(self, chat_id, session_id):

        if not  await self.bot.store.game.check_user_session_reade_to_play(session_id, ready_to_play=True):
            await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text= f'{BotMsg.TimeoutWaitJoin.value}') 
            await self.bot.store.game.update_status_session(session_id, StateEnum.Interrupted)
            await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text= f'{BotMsg.TimeoutWaitJoinNoReade.value}')
             
        elif await self.bot.store.game.check_session(session_id, StateEnum.Established ):
            await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text= f'{BotMsg.TimeoutWaitJoin.value}') 
            await self.bot.store.game.update_status_session(session_id, StateEnum.Active) 

            all_user_session =  await self.bot.store.game.check_all_user_session(session_id) 
            text = f"Участники игры: \n {list_user_session(all_user_session)}, \n набор игроков в команду закрыт!"

            await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                           text=text,
                                                           reply_markup=InlineKeyboardMarkup(
                                                               inline_keyboard=[BotButtons.BeginBtn.value]))
    
    
    async def join_user_game(self, upd):
        
        chat_id = get_chat_id(upd)
        from_ = get_from_(upd)

        check_game_session = await self.bot.store.game.get_session_in_chat(chat_id, lst_state=[
                                                                                        StateEnum.Established])

        if check_game_session:

            session = await self.bot.store.game.check_session_chat_id(chat_id, StateEnum.Established )

            check_user = await self.bot.store.game.check_user_session(from_.id, session.id)

            all_user_session =  await self.bot.store.game.check_all_user_session(session.id) 

            if check_user:
                print(check_user.is_creator)
                if check_user.is_creator is True:
                    await self.bot.store.game.creator_is_ready(id_=check_user.id,  ready_to_play=True)
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f"{from_.first_name}{BotMsg.JoinUserSession.value}")

                else:                    
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f"{from_.first_name}{BotMsg.AlredyToPlayUser.value}")  
                
            
            
            elif len(all_user_session) == self.bot.config.game.questions:
                await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f"{BotMsg.FullUserSession.value}")  
                
            else: 
                user = await self.bot.store.game.creat_user(from_.id, from_.first_name, from_.username)

                await self.bot.store.game.create_user_session(sessions_id=session.id,
                                                                            users_id=user.id,
                                                                            ready_to_play = True) 
                
                await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f"{from_.first_name}{BotMsg.JoinUserSession.value}")

    async def ready_game(self, upd: UpdateObj):
        chat_id = get_chat_id(upd)
        from_ = get_from_(upd)
        check_game_session = await self.bot.store.game.get_session_in_chat(chat_id, lst_state=[
                                                                                        StateEnum.Established])
        if check_game_session:                                                                                
            master_user = await self.bot.store.game.check_master_session(chat_id)
            session_id = master_user.sessions_id
            master_user_id = await self.bot.store.game.check_user_id(master_user.users_id)

            if master_user_id.tg_id == from_.id:

                await self.close_the_user_sessions(chat_id=chat_id, session_id=session_id)

                await sleep(60)
                await self.close_the_sessions_is_no_active(chat_id, session_id) 
            else:           
                await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f"{from_.first_name}"
                                                            f"{BotMsg.CheckGod.value}"
                                                            f"{master_user_id.first_name}")
                                                       
        
    async def begin_game(self, upd): 
        chat_id = get_chat_id(upd)
        from_ = get_from_(upd)
        global is_awaited
        global tq
        global msg_old
        

        check_game_session = await self.bot.store.game.get_session_in_chat(chat_id, lst_state=[StateEnum.ChoiceOfResponder,
                                                                                        StateEnum.Active,
                                                                                        StateEnum.RypleProcess])

        if check_game_session:
            
            msg = upd.message 
            msg_old = ''
            master_user = await self.bot.store.game.check_master_session(chat_id)

            
            captain = await self.bot.store.game.check_user_session_captain(chat_id)

            status =  await self.bot.store.game.check_sesion_status(master_user.sessions.id)
            all_user_session = await self.bot.store.game.check_all_user_session(master_user.sessions.id)
            
            if master_user.users.tg_id == from_.id and status.status.value == "Активная":
                

                captain = await self.bot.store.game.rand_user_is_captain(master_user.sessions.id)

                await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f'Рандомным капитаном команды будешь ты: {captain.users.first_name}! Теперь эта команда твоя забота)')
                
                # TODO: рандомно выбираем djghjcs
                await self.bot.store.game.rand_questions_for_sessions(self.bot.config.game.questions, master_user.sessions.id)
                
                #TODO: Создаем Раунд.
                
                await self.bot.store.game.add_round(master_user.sessions.id, round_number=1 )
                
                #TODO:Задаем вопрос в чат
                tq = await self.bot.store.game.get_session_question_for_chat()
                await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f'Внимание вопрос:\n \n{tq.question.title}\n \n (У вас 1 минута, чтобы обсудить варианты ответа!)')
                await sleep(60)
                
                
                #TODO: Капитан выбирает отвечающего из списка:
                status =  await self.bot.store.game.check_sesion_status(master_user.sessions.id)
                if status.status.value == "Активная":
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f'{captain.users.first_name} выбери игрока, который даст ответ на заданный вопрос и напиши его имя в чат \n Список игроков: \n {list_user_session(all_user_session)} ')
                
                    await self.bot.store.game.update_status_session(master_user.sessions.id, StateEnum.ChoiceOfResponder)
                
            elif status.status.value == "Выбор отвечающего" and captain.users.username == from_.username:
                is_awaited = msg.text
                
                lst_user = [v.first_name for v in all_user_session]
                if is_awaited in lst_user :
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f'{is_awaited} напиши ваш ответ!')
                    await self.bot.store.game.update_status_session(master_user.sessions.id, StateEnum.RypleProcess)
                    
                    # await sleep(15)
                    # print(msg.text)
                    # print(msg_old)
                    # if msg.text == msg_old or msg_old == '':
                    #     await self.bot.store.tg_client.send_message(chat_id=chat_id,
                    #                                                 text=f'{is_awaited} не дал ответ в течении 15 сек, поэтому бал засчитывается боту! ')
                    #     round = await self.bot.store.game.get_round(master_user.sessions.id)
                    #     await self.bot.store.game.update_round_bot(round.id, round.points_bot+1, round.round_number)
                    #     await  self.bot.store.game.update_session_question_for_chat(tq.question.id)

                    #     # Проверить есть ли победитель по итогам набранных баллов, если да, то вывести победителя и закрыть сессию, нет вывести количество баллов
                    #     round = await self.bot.store.game.get_round(master_user.sessions.id)
                    #     if round.points_team == 6:
                    #         await self.bot.store.tg_client.send_message(chat_id=chat_id,
                    #                                             text=f'Поздравляю вы выиграли! ')
                            
                    #         await self.bot.store.game.update_status_session(master_user.sessions.id, StateEnum.Ended)
                        
                    #     elif round.points_bot == 6:
                    #         await self.bot.store.tg_client.send_message(chat_id=chat_id,
                    #                                             text=f'Ой что то пошло не так и бот выиграл, не расстраивайтесь в следующий раз у вас все получится.')
                            
                    #         await self.bot.store.game.update_status_session(master_user.sessions.id, StateEnum.Ended)
                    #     else:
                    #         await self.bot.store.tg_client.send_message(chat_id=chat_id,
                    #                                             text=f'Счет. \n Команда игроков: {round.points_team} \n Бот: {round.points_bot}')
                        
                    #     status =  await self.bot.store.game.check_sesion_status(master_user.sessions.id)
                    #     if status.status.value != "Законченная":
                    #         # создать новый раунд +1 от предыдущего
                    #         round = await self.bot.store.game.get_round(master_user.sessions.id)        
                    #         await self.bot.store.game.add_round(master_user.sessions.id, points_team=round.points_team, points_bot=round.points_bot, round_number=round.round_number + 1, responsible=False )
                            
                    #         # задать вопрос
                            
                    #         tq= await self.bot.store.game.get_session_question_for_chat()
                    #         print(tq)
                    #         await self.bot.store.tg_client.send_message(chat_id=chat_id,
                    #                                                 text=f'Внимание вопрос:\n \n{tq.question.title} \n \n У вас 1 минута, чтобы обсудить варианты ответа!')
                    #         await sleep(60)
                            
                    #         # update статус сесии на ChoiceOfResponder   
                    #         await self.bot.store.tg_client.send_message(chat_id=chat_id,
                    #                                                 text=f'{captain.users.first_name} выбери игрока, который даст ответ на заданный вопрос и напиши его никнейм в чат \n Список игроков: \n {list_user_session(all_user_session)} ')
                            
                    #         await self.bot.store.game.update_status_session(master_user.sessions.id, StateEnum.ChoiceOfResponder)
                    # msg_old=msg.text         
                            
            elif status.status.value == "Ожидание ответа" and is_awaited==from_.first_name:

                
                round = await self.bot.store.game.get_round(master_user.sessions.id)
                
                answer = await self.bot.store.game.get_answer(tq.question.id)
                #проверить ответ
                # начислить баллы

                if msg.text in answer:
                    await self.bot.store.game.update_round_user(round.id, round.points_team+1, round.round_number)
                else:
                    await self.bot.store.game.update_round_bot(round.id, round.points_bot+1, round.round_number)
                
                await  self.bot.store.game.update_session_question_for_chat(tq.question.id)
                # Проверить есть ли победитель по итогам набранных баллов, если да, то вывести победителя и закрыть сессию, нет вывести количество баллов
                round = await self.bot.store.game.get_round(master_user.sessions.id)
                if round.points_team == 6:
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f'Поздравляю вы выиграли! ')
                    
                    await self.bot.store.game.update_status_session(master_user.sessions.id, StateEnum.Ended)
                
                elif round.points_bot == 6:
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f'Ой что то пошло не так и бот выиграл, не расстраивайтесь в следующий раз у вас все получится.')
                    
                    await self.bot.store.game.update_status_session(master_user.sessions.id, StateEnum.Ended)
                else:
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                        text=f'Счет. \n Команда игроков: {round.points_team} \n Бот: {round.points_bot}')
                status =  await self.bot.store.game.check_sesion_status(master_user.sessions.id)
                if status.status.value != "Законченная": ######
                    # создать новый раунд +1 от предыдущего
                    round = await self.bot.store.game.get_round(master_user.sessions.id)        
                    await self.bot.store.game.add_round(master_user.sessions.id, points_team=round.points_team, points_bot=round.points_bot, round_number=round.round_number + 1, responsible=False )
                    
                    # задать вопрос
                    
                    tq= await self.bot.store.game.get_session_question_for_chat()
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                            text=f'Внимание вопрос:\n \n{tq.question.title} \n \n У вас 1 минута, чтобы обсудить варианты ответа!')
                    
                    await sleep(60)
                    status =  await self.bot.store.game.check_sesion_status(master_user.sessions.id)
                    if status.status.value == "Ожидание ответа": 
                    # update статус сесии на ChoiceOfResponder   
                        await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                            text=f'{captain.users.first_name} выбери игрока, который даст ответ на заданный вопрос и напиши его никнейм в чат \n Список игроков: \n {list_user_session(all_user_session)} ')
                    
                        await self.bot.store.game.update_status_session(master_user.sessions.id, StateEnum.ChoiceOfResponder)
                
    async def bot_stop_game(self, upd): 
        chat_id = get_chat_id(upd)
        from_ = get_from_(upd)      

        session = await self.bot.store.game.get_session_not_in_lst_state(chat_id=chat_id,
                                                                          lst_state=[StateEnum.Ended,
                                                                                     StateEnum.Interrupted])  
       
        if session:
            master_user = await self.bot.store.game.check_master_session(chat_id)
            if master_user.users.tg_id == from_.id:
                result = await self.bot.store.game.get_round(master_user.sessions.id) 
                check = await self.bot.store.game.check_round_for_existence(master_user.sessions.id)
                print(check)
                if not check:
                    await self.bot.store.game.update_status_session_end(master_user.sessions.id, StateEnum.Ended, end_date=datetime.utcnow(), result=ResultEnum.Not)
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                         text=f"{BotMsg.StopByGod.value} "
                                                              f"{master_user.users.first_name} \n"
                                                              f"Игра закончилась не успев начаться, победивших увы нет!")

                elif result.points_team > result.points_bot:
                    await self.bot.store.game.update_status_session_end(master_user.sessions.id, StateEnum.Ended, end_date=datetime.utcnow(), result=ResultEnum.Users)
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                         text=f"{BotMsg.StopByGod.value} "
                                                              f"{master_user.users.first_name} \n"
                                                              f"Победила команда игроков!") 

                elif result.points_team == 0 and result.points_bot == 0:
                    await self.bot.store.game.update_status_session_end(master_user.sessions.id, StateEnum.Ended, end_date=datetime.utcnow(), result=ResultEnum.Not)
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                         text=f"{BotMsg.StopByGod.value} "
                                                              f"{master_user.users.first_name} \n"
                                                              f"Игра закончилась не успев начаться, победивших увы нет!")

                else:
                    await self.bot.store.game.update_status_session_end(master_user.sessions.id, StateEnum.Ended, end_date=datetime.utcnow(), result=ResultEnum.Bot)
                    await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                         text=f"{BotMsg.StopByGod.value} "
                                                              f"{master_user.users.first_name} \n"
                                                              f"Победил бот!") 
                    
                
            else:
                await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                         text=f"{from_.first_name}"
                                                              f"{BotMsg.UserGod.value}"
                                                              f"{master_user.users.first_name}")
        else:
            await self.bot.store.tg_client.send_message(chat_id=chat_id,
                                                     text=BotMsg.SessionNoActive.value)

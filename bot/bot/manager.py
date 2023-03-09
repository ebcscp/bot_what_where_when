from urllib.parse import urljoin
import requests
import json
import typing
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from database.database import Database
from dataclasses_models import UpdateObj
from bot.enum_blanks import BotMsg, BotButtons, StatusAddBot
from game.models import Answer, Question, StateEnum


class BotAccessor(Database):
    def __init__(self, bot: "Worker",  *args, **kwargs):
        self.bot = bot

    async def _get_admin_worker(self, chat_id: int, url: str = ' ' ):
        if chat_id == 1079223049:
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
        await self.bot.tg_cli.send_message(chat_id=chat_id,
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

        check_game_session = self.bot.pgcli.get_session_in_chat(chat_id)

        if check_game_session:
            await self.send_keyboard(chat_id=chat_id, text=BotMsg.GameSessionActive.value)
        else:
            from_ = upd.callback_query.from_ if upd.callback_query else upd.message.from_
            
            user = await self.bot.game.creat_user_session(from_.id, from_.first_name, from_.username)
            print(user)
            
            new_session = await self.bot.store.game.create_game_session(chat_id=chat_id,
                                                                   state=StateEnum.Active)
            user_session = await self.bot.store.game.create_user_session(session_id=new_session.id,
                                                                   user_id=user.id,
                                                                   is_master=True)

            await self.send_keyboard(chat_id=chat_id,
                                     text=BotMsg.MenuDescription.value)
            # TODO: вывести правила игры + кнопки: "Я участвую" и "Завершить набор"
            des_mes = await self.bot.store.tg_cli.send_message(chat_id=chat_id,
                                                               text=f"{BotMsg.GameRules.value} \n\n"
                                                                    f"Игровой мастер: {user.first_name}",
                                                               reply_markup=InlineKeyboardMarkup(
                                                                   inline_keyboard=[BotButtons.JoinBtns.value]))    

            
            # 1) Создавать первого пользака, как мастера, при этом чекнув есть ли он в базе, если нет добавить в таблицу users!
            # 2) Остальных пользователей добавлять также с проверкой, НО БЕЗ МАСТЕРА и автоматчиески закидывать в игровую сессию
            # 3) 6 игроков максимум!
            # 4) Рандомный капитан каманда!
            # 5) Подумать как выбирать отвечающего...
            # 6) Тайминги
            # 7) Рандомно выбрать 11 вопросов!
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

        check_game_session = self.bot.pgcli.get_gs_in_chat(chat_id)

        if check_game_session:
            await self.send_keyboard(chat_id=chat_id, text=BotMsg.GameSessionActive.value)
        else:
            from_ = upd.callback_query.from_ if upd.callback_query else upd.message.from_

            player = await self.bot.game.creat_user_session(from_.id, from_.first_name, from_.username)


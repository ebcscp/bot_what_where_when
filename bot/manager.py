from urllib.parse import urljoin
import requests
import json
import typing

from admin.models import Answer, Question
from tg_api import TgClient
from admin.accessor import AdminAccessor

class TgApiAccessor():
    def __init__(self, bot: "Worker",  *args, **kwargs):
        self.bot = bot

    async def connect(self):
        pass

    async def disconnect(self):
        pass
            
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

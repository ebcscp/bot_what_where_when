from json import JSONDecodeError
from typing import Optional, List
import typing
import aiohttp
from marshmallow.exceptions import ValidationError

from models import  Message, SendMessageResponse, GetFileResponse, File

if typing.TYPE_CHECKING:
    from worker import Worker


class TgClientError(Exception):
    pass

class TgClient:
    def __init__(self, bot: "Worker"):
        self.token = bot.config.tg_config.token
        self.api_path = bot.config.tg_config.api_path
        self.bot = bot

    def get_base_path(self):
        return f'{self.api_path}/bot{self.token}'

    async def _handle_response(self, resp):
        if resp.status != 200:
            raise TgClientError
        try:
            return await resp.json()
        except JSONDecodeError:
            raise TgClientError

    async def send_message(self, chat_id: int, text: str) -> Message:
        url = self.get_base_path() + '/sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                res_dict = await self._handle_response(resp)
                try:
                    sm_response: SendMessageResponse = SendMessageResponse.Schema().load(res_dict)
                except ValidationError:
                    raise TgClientError
                return sm_response.result
            
    async def get_file(self, file_id: str) -> File:
        url = self.get_base_path() + '/getFile' 
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={'file_id': file_id}) as resp:
                res=await self._handle_response(resp)
                try:
                    gf_response: GetFileResponse = GetFileResponse.Schema().load(res)
                except ValidationError:    
                    raise TgClientError
                return gf_response.result
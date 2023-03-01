from json import JSONDecodeError
from typing import Optional, List

import aiohttp
from marshmallow.exceptions import ValidationError

from worker.models import  Message, SendMessageResponse



class TgClientError(Exception):
    pass

class TgClient:
    API_PATH = 'https://api.telegram.org'

    def __init__(self, token: str = ''):
        self.token = "6291132929:AAGe2sRTPRxG6WLWn0RqQmi-8mFqYXuUWZM"

    def get_base_path(self):
        return f'{self.API_PATH}/bot{self.token}'

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

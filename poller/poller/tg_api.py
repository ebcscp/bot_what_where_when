from typing import Optional, List, Any

from json import JSONDecodeError
from poller.poller.models import UpdateObj, Message, GetUpdatesResponse, GetFileResponse, SendMessageResponse
import aiohttp
from marshmallow.exceptions import ValidationError


class TgClientError(Exception):
    pass


class TgClient:    
    def __init__(self, token: str = '', api_path: str =''):
        self.token = token
        self.session = aiohttp.ClientSession()
        self.api_path = api_path    
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()    

    async def _handle_response(self, resp):
        if resp.status !=200:
            raise TgClientError
        try:            
            return await resp.json()
        except JSONDecodeError:
            raise TgClientError

    def get_path(self):
        return f'{self.api_path}{self.token}'

    async def get_me(self) -> dict:
        url = self.get_path() + '/getMe'
        async with self.session.get(url) as resp:
            return await self._handle_response(resp)

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        url = self.get_path() + '/getUpdates'
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout  
        async with self.session.get(url, params=params) as resp:
            return await self._handle_response(resp)

    async def get_updates_in_objects(self, *args, **kwargs) -> List[UpdateObj]:
        res_dict = await self.get_updates(*args, **kwargs)
        print(res_dict)
        try:
            gu_response: GetUpdatesResponse = GetUpdatesResponse.Schema().load(res_dict)
        except ValidationError:    
            raise TgClientError
        return gu_response.result

    async def send_message(self, chat_id: int, text: str) -> Message:
        url = self.get_path() + '/sendMessage'
        pay_load = {
            'chat_id': chat_id,
            'text': text
        }
        async with self.session.post(url, json=pay_load) as resp:
            res_dict =  await self._handle_response(resp)
            try:
                sm_response: SendMessageResponse = SendMessageResponse.Schema().load(res_dict)
            except ValidationError:    
                raise TgClientError
            return sm_response.result
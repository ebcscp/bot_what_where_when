import typing
from typing import Optional
from urllib.parse import urljoin
from webbrowser import get

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from database.base_accessor import BaseAccessor
from admin.models import Answer, Question
from worker.tg_api import TgClient


class TgApiAccessor(TgClient):
    def __init__(self, *args, **kwargs):
        pass

    async def connect(self):
        pass

    async def disconnect(self):
        pass
            
    async def _get_worker(self, chat_id: int, text: str):
        if chat_id == 1079223049:
            if text == '/admin':
                return "Добро пожаловать в админку!"  
            elif text == '/create_question':
                self.send_message()
                return "Введите "                  
            else:
                return "В разработке"
        else:
            return "Не верный чат id"        
      
    # async def distribution(self, data):    
    #     updates = []
    #     for update in data['updates']:           
    #         if update.get('type') == 'message_new': 
    #             peer_id = update.get('object', {}).get('message', {}).get('peer_id')
    #             from_id = update.get('object', {}).get('message', {}).get('from_id')
                
    #             if update.get('object', {}).get('message', {}).get('action',{}).get('type') == 'chat_invite_user':
    #                 m = update.get('object', {}).get('message', {}).get('action',{}).get('member_id')              
    #                 profiles = await self.app.store.context.get_conversation_members(m, self.session)                       
    #                 updates = Users(vk_id= profiles[0]['id'],
    #                             chat_id=peer_id,
    #                             first_name= profiles[0]['first_name'],
    #                             last_name= profiles[0]['last_name'],
    #                             is_staff= False                                
    #                         )
    #                 await self.app.store.user.add_user_manager(updates)
                    
    #             elif update.get('object', {}).get('message', {}).get('text', {}) == 'photo':
    #                 async with self.session.get(urljoin(API_PATH, "messages.getConversationMembers"), 
    #                                 params={
    #                                         "peer_id":peer_id, 
    #                                         "fields": 'photo_id',
    #                                         "access_token": self.app.config.bot.token,
    #                                         "v":self.app.config.bot.v, 
    #                                         },
    #                     ) as resp:
    #                         data = (await resp.json())['response']
    #                         s = dict()
    #                         for profiles in data['profiles']:
    #                             print(profiles)
    #                             s[profiles.get('id')] = 'photo'+ profiles.get('photo_id')

                            
    #             elif update.get('object', {}).get('message', {}).get('text', {}) == 'test': 
    #                     message = 'Началась новая игровая сессия!'
    #                     #бот создает сессию
    #                     session_game = await self.app.store.session.create_session(peer_id)
                        
    #                     #добавляет пользователей в новую игровую сессию
    #                     await self.app.store.session_users.user_migration(peer_id, session_game)
                        
    #                     async with self.session.get(urljoin(API_PATH, "messages.getConversationMembers"), 
    #                                 params={
    #                                         "peer_id":peer_id, 
    #                                         "fields": 'photo_id',
    #                                         "access_token": self.app.config.bot.token,
    #                                         "v":self.app.config.bot.v, 
    #                                         },
    #                     ) as resp:
    #                         data = (await resp.json())['response']
    #                         s = dict()
    #                         for profiles in data['profiles']:
    #                             print(profiles)
    #                             s[profiles.get('id')] = 'photo'+ profiles.get('photo_id')  
                        
    #                     #добавление пользователей в round
    #                     await self.app.store.rounds.session_round(session_game, self.session, peer_id, s, update) 
                         
                    
    #             elif update.get('object', {}).get('message', {}).get('text', {}) == 'start':                 
    #                 if await self.app.store.session.select_session(peer_id, 'Активная'):
    #                         message = 'Игровая сессия уже запущена, дождитесь завершения! Либо для эсктренного завершения игры, напишите в чат команду stop.'
    #                         await self.app.store.context.send_message(peer_id, self.session, message)
    #                 else:
    #                     message = 'Началась новая игровая сессия!'
    #                     #бот создает сессию
    #                     session_game = await self.app.store.session.create_session(peer_id)
                        
    #                     #добавляет пользователей в новую игровую сессию
    #                     await self.app.store.session_users.user_migration(peer_id, session_game)
                        
    #                     #сообщение о начале игровой сессии
    #                     await self.app.store.context.send_message(peer_id, self.session, message)
                        
    #                     #добавлени игроков в раунд
    #                     await self.app.store.rounds.session_round(peer_id)
                        
    #                     #завершение игровой сессии
    #                     await self.app.store.session.stop_session(peer_id)
                        
    #             elif update.get('object', {}).get('message', {}).get('text', {}) == 'stop':
    #                 if await self.app.store.session.select_session(peer_id,'Законченная'):
    #                     message = 'Игровая сессия не активна! Для запуска новой игровой сессии напишите в чат start.'
    #                     await self.app.store.context.send_message(peer_id, self.session, message)
    #                 else:  
    #                     message = 'Игровая сессия завершена!'    
    #                     await self.app.store.session.stop_session(peer_id)
    #                     await self.app.store.context.send_message(peer_id, self.session, message)


    
    # async def send_message(self, message: Message) -> None:
    #     print(message)
    #     async with self.session.get(urljoin(API_PATH, "messages.send"), 
    #                                 params={
    #                                         "peer_id": message.peer_id, 
    #                                         "random_id": random.randint(1, 2**32), 
    #                                         "peer_id":message.peer_id, #"-" + str(self.app.config.bot.group_id),
    #                                         "message": message.text,
    #                                         "disable_mentions":1,
    #                                         "keyboard":open("app/vk_api/keyboard.json", "r", encoding="UTF-8").read() ,#await self.app.store.bots_manager.get_keys(),
    #                                         "access_token": self.app.config.bot.token,
    #                                         "v":self.app.config.bot.v, 
    #                                         },
    #     ) as resp:
    #         data = await resp.json()
    #         self.logger.info(data)
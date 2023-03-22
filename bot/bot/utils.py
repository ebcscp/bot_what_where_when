from telegram import InlineKeyboardButton

def list_user_session_awaited(players: list):
    return [InlineKeyboardButton(v.first_name, callback_data=v.first_name)  for v in players]

def list_user_session(players: list):
    return " ".join([f"{c}. {v.first_name} \n" for c, v in enumerate(players, start=1)])

def get_chat_id(upd):
    return upd.callback_query.message.chat.id if upd.callback_query else upd.message.chat.id

def get_from_(upd):
    return upd.callback_query.from_ if upd.callback_query else upd.message.from_

def get_call_msg(upd):
    return upd.callback_query.data  if upd.callback_query else None
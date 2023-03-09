from enum import Enum, IntEnum

from telegram import InlineKeyboardButton


class BotMsg(Enum):
    add =  f"Привет! Я бот игры 'Что? Где? Когда?', если хочешь поиграть просто нажми 'СТАРТ'! "
    GameSessionActive = "В чате уже есть активная игра."
    
class StatusAddBot(Enum):
    Member = "member"
    Left = "left"

    
class Commands(Enum):
    Stop = "/stop"
    Start = "/start"
    GameInform = '/game_inform'
    GeneralRating = '/general_rating'


class CallBackData(Enum):
    Start = "/start"
    IJoin = "/IJoin"
    WeReady = "/WeReady"
    Go = "/Go"


class BotButtons(Enum):
    StartBtn = [InlineKeyboardButton("СТАРТ", callback_data=CallBackData.Start.value)]
    BeginBtn = [InlineKeyboardButton("Начать игру!", callback_data=CallBackData.Go.value)]
    Keyboard = [[Commands.Start.value], [Commands.Stop.value], [Commands.GameInform.value],
                [Commands.GeneralRating.value]]
    JoinBtns = [InlineKeyboardButton("Я участвую!", callback_data=CallBackData.IJoin.value),
                InlineKeyboardButton("Завершить набор", callback_data=CallBackData.WeReady.value)]
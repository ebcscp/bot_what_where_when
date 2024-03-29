from dataclasses import dataclass
from database.sqlalchemy_base import db
from datetime import datetime
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey, VARCHAR, DateTime, BigInteger, Enum
from sqlalchemy.orm import relation
from enum import  Enum as enum

@dataclass
class User:
    id: int
    tg_id: int
    first_name: str
    username: str

@dataclass
class UserSession:
    id: int
    id_session: int
    id_user: int
    is_creator: bool
    is_captain: bool
    ready_to_play: bool

@dataclass
class Session:
    id: int
    id_chat: int
    start_date: datetime 
    end_date: datetime 
    status: str
    result: str

class StateEnum(enum):
    Active = "Активная"
    Ended = "Законченная"
    Established = "Создана"
    ChoiceOfResponder = "Выбор отвечающего"
    RypleProcess = "Ожидание ответа"
    Interrupted = "Прерванная"
    Discussion = "Обсуждение вопроса"

class ResultEnum(enum):
    Users = "Команда игроков"
    Bot = "Бот"
    Not = "Нет победителя"




@dataclass
class Round:
    id: int
    id_session: int  
    points_team: int
    points_bot: int
    round_number: int
    responsible: bool
    is_awaited: str

@dataclass
class SessionQuestion:
    id: int
    id_session: int    
    id_question: int
    is_answerd: bool


@dataclass
class Question:
    id: int 
    title: str
    answers: list["Answer"]

@dataclass
class Answer:
    title: str


class UsersModel(db):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    first_name = Column(VARCHAR(50), nullable=False)
    username = Column(VARCHAR)

    user_sessions = relation("SessionUsersModel", back_populates="users")

class SessionUsersModel(db):
    __tablename__ = "session_users" 
    id = Column(Integer, primary_key=True)

    sessions_id = Column(BigInteger, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    users_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    ready_to_play = Column(Boolean)
    sessions = relation("SessionsModel", back_populates="user_sessions")
    users = relation("UsersModel", back_populates="user_sessions")

    is_creator = Column(Boolean, default=False)
    is_captain = Column(Boolean, default=False)

class SessionsModel(db):
    __tablename__ = "sessions" 
    id = Column(Integer, primary_key=True) 
    id_chat = Column(BigInteger) 
    start_date = Column(DateTime, default=datetime.utcnow())
    end_date = Column(DateTime)
    status = Column(Enum(StateEnum), default=StateEnum.Active) 
    result = Column(Enum(ResultEnum))

    user_sessions = relation("SessionUsersModel", back_populates="sessions")
    rounds = relation("RoundsModel", back_populates="sessions")
    session_question = relation("SessionQuestionModel", back_populates="sessions") ###


class RoundsModel(db):
    __tablename__ = "rounds"       
    id = Column(Integer, primary_key=True)
    id_session = Column(Integer, ForeignKey("sessions.id")) 
    points_team = Column(Integer)
    points_bot = Column(Integer)
    round_number = Column(Integer)
    responsible = Column(Boolean)
    is_awaited = Column(VARCHAR(200))

    sessions = relation("SessionsModel", back_populates= "rounds")
 

class SessionQuestionModel(db):
    __tablename__ = "session_question" 
    id = Column(Integer, primary_key=True)
    id_session = Column(Integer, ForeignKey("sessions.id")) 
    id_qusetion = Column(Integer, ForeignKey("question.id")) 
    is_answerd = Column(Boolean)  

    sessions = relation("SessionsModel", back_populates="session_question")
    question = relation("QuestionModel", back_populates="session_question")

class QuestionModel(db):
    __tablename__ = "question"    
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(200))
    answer = relation("AnswerModel", back_populates="question")

    session_question = relation("SessionQuestionModel", back_populates='question')


class AnswerModel(db):
    __tablename__ =  "answer"
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"), nullable=False) 
    title = Column(VARCHAR(200))    

    question = relation("QuestionModel", back_populates = "answer" )
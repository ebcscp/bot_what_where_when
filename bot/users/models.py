from dataclasses import dataclass
from database.sqlalchemy_base import db
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey, VARCHAR, DateTime
from sqlalchemy.orm import relationship

@dataclass
class User:
    id: int
    tg_id: int
    chat_id: int
    first_name: str
    last_name: str

@dataclass
class Session:
    id: int
    id_chat: int
    date_start: DateTime
    date_expiration: DateTime
    status: str
    session_result: str

@dataclass
class UserSession:
    id: int
    id_session: int
    id_user: int
    status_user: str

@dataclass
class Round:
    id: int
    id_session: int    
    number_of_point_users: int
    number_of_point_bot: int
    number_of_round: int

@dataclass
class SessionQuestion:
    id: int
    id_session: int    
    id_question: int
    is_answerd: str


@dataclass
class Question:
    id: int 
    title: str
    answers: list["Answer"]

@dataclass
class Answer:
    id:int
    question_id:int
    title: str


class SessionsModel(db):
    __tablename__ = "sessions" 
    id = Column(Integer, primary_key=True) 
    id_chat = Column(Integer) 
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(VARCHAR(20))  

class SessionQuestionModel(db):
    __tablename__ = "session_users" 
    id = Column(Integer, primary_key=True)
    id_session = Column(Integer, ForeignKey("sessions.id")) 
    id_session = Column(Integer)  
    is_answerd = Column(VARCHAR(50))  

class SessionUsersModel(db):
    __tablename__ = "session_users" 
    id = Column(Integer, primary_key=True)
    id_session = Column(Integer, ForeignKey("sessions.id")) 
    id_user = Column(Integer, ForeignKey("users.id"))  
    status_user = Column(Boolean) 


class RoundsModel(db):
    __tablename__ = "rounds"       
    id = Column(Integer, primary_key=True)
    id_session = Column(Integer, ForeignKey("sessions.id")) 
    id_user = Column(Integer, ForeignKey("users.id"))
    id_rival = Column(Integer)
    points = Column(Integer)
    round_number = Column(VARCHAR(3))
    result = Column(VARCHAR(20))

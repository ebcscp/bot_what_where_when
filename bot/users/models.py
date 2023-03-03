from dataclasses import dataclass
from database.sqlalchemy_base import db
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey, VARCHAR, DateTime
from sqlalchemy.orm import relationship

@dataclass
class Theme:
    id: int 
    title: str


@dataclass
class Question:
    id: int 
    title: str
    theme_id: int
    answers: list["Answer"]


@dataclass
class Answer:
    title: str
    is_correct: bool

###################3

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
class Question:
    id: int 
    title: str
    answers: list["Answer"]

@dataclass
class Answer:
    id:int
    question_id:int
    title: str


#######################33

class QuestionModel(db):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(200), nullable=False, unique=True)
    answers = relationship("AnswerModel", back_populates="question")


class AnswerModel(db):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(250), nullable=False, unique=True)
    question_id = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"), nullable=False)
    question = relationship("QuestionModel", back_populates="answer")

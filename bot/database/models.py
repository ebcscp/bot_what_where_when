from dataclasses import dataclass
from bot.database.sqlalchemy_base import db
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey, VARCHAR, DateTime
from sqlalchemy.orm import relation

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
class User(db):
    __tablename__="user"
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    first_name = Column(VARCHAR(50))
    last_name = Column(VARCHAR(50))

class Session(db):
    id = Column(Integer, primary_key=True)
    id_chat = Column(Integer)
    date_start = Column(DateTime)
    date_expiration = Column(DateTime)
    status = Column(VARCHAR(20))
    session_result = Column(VARCHAR(20))

class ThemeModel(db):
    __tablename__ = "themes"
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(200), nullable=False, unique=True)
    questions = relation("QuestionModel", back_populates="theme")


class QuestionModel(db):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(200), nullable=False, unique=True)
    theme_id = Column(Integer, ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)
    answers = relation("AnswerModel", back_populates="question")
    theme = relation("ThemeModel", back_populates="questions")


class AnswerModel(db):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(250), nullable=False, unique=True)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    question = relation("QuestionModel", back_populates="answers")
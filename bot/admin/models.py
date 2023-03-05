from dataclasses import dataclass
from database.sqlalchemy_base import db
from sqlalchemy import Column, Integer,String,Boolean, ForeignKey, VARCHAR, DateTime
from sqlalchemy.orm import relation

from sqlalchemy.orm import relation


@dataclass
class Question:
    id: int 
    title: str
    answers: list["Answer"]

@dataclass
class Answer:
    # id:int
    # question_id:int
    title: str


#######################33

class QuestionModel(db):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(200), nullable=False, unique=True)
    answer = relation("AnswerModel", back_populates="question")


class AnswerModel(db):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(250), nullable=False, unique=True)
    question_id = Column(Integer, ForeignKey("question.id", ondelete="CASCADE"), nullable=False)
    question = relation("QuestionModel", back_populates="answer")

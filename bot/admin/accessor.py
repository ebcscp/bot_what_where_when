from database.database import Database
import typing
from game.models import AnswerModel, QuestionModel, Answer, Question
from sqlalchemy import select as Select
from sqlalchemy.orm import joinedload
from store import Database

class AdminAccessor(Database):
    def __init__(self, bot: "Worker"):
        self.bot = bot
    async def create_answers(
        self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        #res_answers = []
        for answer in answers:
            answer_model = AnswerModel(title=answer.title,
                                       question_id=question_id,
                                  )
            await self.bot.pgcli.insert(answer_model)
            
            #res_answers.append(answer)
        #return res_answers
    
    async def create_question(
        self, title: str, answers: list[Answer]
    ) -> Question:
        question_model = QuestionModel(title=title)
        await self.bot.pgcli.insert(question_model)
        question = Question(
            id=question_model.id,
            title=question_model.title,
            answers=answers
        )
        await self.create_answers(question.id, answers)
        #return await self.get_question_by_title(title)        
    
    # async def get_question_by_title(self, title: str) -> Question:
    #     question_model = Select(QuestionModel).where(QuestionModel.title == title).options(joinedload(QuestionModel.answers))
    #     res = await self.bot.pgcli.select(question_model)

    #     question = None
    #     raw_question = res.first()
        
    #     if raw_question:
    #         question = Question(id=raw_question[0].id,
    #                             title=raw_question[0].title,
    #                             theme_id=raw_question[0].theme_id,
    #                             answers=[Answer(a.title, a.is_correct) for a in raw_question[0].answers])
    #     return question

        
    # async def list_questions(self, theme_id: int | None = None) -> list[Question]:
    #     list_questions = []
    #     question_model = Select(QuestionModel).options(joinedload(QuestionModel.answers))

    #     if theme_id:
    #         check_theme = await self.get_theme_by_id(theme_id)
    #         if check_theme:
    #             question_model = Select(QuestionModel).where(QuestionModel.theme_id == theme_id) \
    #                 .options(joinedload(QuestionModel.answers))

    #     res = await self.select(question_model)
    #     raw_questions = res.scalars().unique()
    #     if raw_questions:
    #         for raw_question in raw_questions:
    #             list_questions.append(Question(id=raw_question.id,
    #                                            title=raw_question.title,
    #                                            theme_id=raw_question.theme_id,
    #                                            answers=[Answer(a.title, a.is_correct) for a in
    #                                                     raw_question.answers]))

    #     return list_questions
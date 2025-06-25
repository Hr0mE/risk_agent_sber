from pydantic import BaseModel, Field
from typing import List


class QuestionDecompositionModel(BaseModel):
    """Анализ вопроса пользователя, разбиение на подвопросы"""

    raw_question: str = Field(
        description="Дословный оригинал вопроса пользователя"
    )

    thoughts: str = Field(
        description=(
            "Анализ скрытых мотивов, возможных когнитивных искажений и "
            "невысказанных предпосылок (3-5 предложений)"
        )
    )

    problem: str = Field(
        description="Ключевая проблема в формулировке 'как + инфинитив + контекст'",
    )

    problem_solving_question: str = Field(
        description="Переформулированный вопрос, решающий корневую проблему",
    )

    sub_questions: List[str] = Field(
        description="Цепочка логически связанных уточняющих вопросов"
    )

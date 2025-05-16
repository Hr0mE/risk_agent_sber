from pydantic import BaseModel, Field
from typing import List

class QuestionDecompositionModel(BaseModel):
    """Анализ вопроса пользователя, разбиение на подвопросы"""

    raw_question: str = Field(
        description="Дословный оригинал вопроса пользователя",
        example="Почему Python медленнее Java?"
    )
    
    thoughts: str = Field(
        description=(
            "Анализ скрытых мотивов, возможных когнитивных искажений и "
            "невысказанных предпосылок (3-5 предложений)"
        ),
        example="Пользователь может подразумевать выбор языка для высоконагруженной системы..."
    )
    
    problem: str = Field(
        description="Ключевая проблема в формулировке 'как + инфинитив + контекст'",
        example="как выбрать язык программирования для задач real-time обработки данных"
    )
    
    problem_solving_question: str = Field(
        description="Переформулированный вопрос, решающий корневую проблему",
        example="Какие критерии сравнения языков программирования важны для систем real-time?"
    )
    
    sub_questions: List[str] = Field(
        description="Цепочка логически связанных уточняющих вопросов",
        examples=[
            [
                "Какие аспекты производительности критичны для real-time систем?",
                "Как сравнивать языки по latency и throughput?",
                "Какие инструменты бенчмаркинга дают объективные метрики?"
            ]
        ]
    )


from typing import Dict, List
from langgraph.graph import MessagesState
from .validation_models import MannerInfo, FAQData, Question


class GlobalState(MessagesState):
    problem_solving_question: (
        str  # Вопрос из ноды QuestionDecomposition, который поможет решить проблему пользователя
    )
    sub_questions: List[str]  # Подвопросы из ноды QuestionDecomposition
    last_reason: str # Последние рассуждение ноды reason
    user_question: str # вопрос пользователя
    last_answer: str # Последний ответ ноды write
    critique: List[str] # Последняя критика ноды Critic
    final_decision: str # Решение Critic
    final_answer: str # Текст, который из Critic идёт в Finalize
    search_query: str # Поисковый запрос в ноду Search
    search_results: Dict # Результат поискового запроса
    rag_query: str # Запрос в ноду Rag для поиска по внутренним документам 
    rag_results: Dict # Результат rag-запроса

    is_info_in_memory: bool  # Есть ли манера в памяти
    is_write_to_memory: bool  # Надо ли записывать манеру в память
    manner: MannerInfo  # Данные о манере
    remaining_steps_to_check_manner: int  # Подсчет кол-ва шагов для адаптации
    # raw_questions: List[str]  # Буфер вопросов для извлечения
    raw_questions: List[Question]  # Буфер вопросов для извлечения
    # faq: List[Dict[str, List[str]]]  # Извлеченные часто задаваемые вопросы, сгруппированые по тематикам
    faq: List[FAQData]  # Извлеченные часто задаваемые вопросы, сгруппированые по тематикам
    is_write_faq: bool  # Надо ли записывать FAQ в память

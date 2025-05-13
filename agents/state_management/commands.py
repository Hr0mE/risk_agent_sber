from enum import Enum
from typing import NamedTuple, Dict

class NodeMeta(NamedTuple):
    label: str  # Человекочитаемое название
    description: str  # Описание назначения ноды
    emoji: str = ""  # Опциональная иконка

class NodeNames(str, Enum):
    """Все зарегистрированные ноды в системе"""
    EXTRACT_MANNER = "extract_manner"
    WRITE_MANNER = "wrtie_manner_to_memory"
    GET_MANNER = "extract_manner_from_memory"
    STORE_QUESTION = "store_question"
    EXTRACT_FAQ = "extract_faq"
    WRITE_FAQ = "write_faq_to_memory"
    GET_FAQ = "extract_faq_from_memory"
    REASON = "reason"
    FIRST_STEP = "first_step"
    SEARCH = "search"
    RAG = "rag"
    WRITE = "write"
    FINALIZE = "finalize"
    CRITIQUE = "critic"

    @property
    def meta(self) -> NodeMeta:
        return NODE_METADATA[self]

# Регистрируем метаданные отдельно от логики
NODE_METADATA: Dict[NodeNames, NodeMeta] = {
    NodeNames.EXTRACT_MANNER: NodeMeta(
        label="Извлечение манеры",
        description="Извлечение манеры пользователя из запроса",
        emoji="👩‍🔬"
    ),
    NodeNames.WRITE_MANNER: NodeMeta(
        label="Запись манеры",
        description="Запись полученной манеры пользователя в память",
        emoji="📝"
    ),
    NodeNames.GET_MANNER: NodeMeta(
        label="Получение манеры",
        description="Извлечение манеры пользователя из памяти",
        emoji="💭"),
    NodeNames.STORE_QUESTION: NodeMeta(
        label="Сбор вопросов",
        description="Сбор вопросов во временный буфер",
        emoji="❓"),
    NodeNames.EXTRACT_FAQ: NodeMeta(
        label="Извлечение вопросов",
        description="Извлечение часто задаваемых вопросов + сортировка по тематикам",
        emoji="👩‍🔬"),
    NodeNames.WRITE_FAQ: NodeMeta(
        label="Запись вопросов",
        description="Запись часто задаваемых вопросов по тематикам в память",
        emoji="📝"),
    NodeNames.GET_FAQ: NodeMeta(
        label="Извлчение вопросов",
        description="Извлечение часто задаваемых вопросов",
        emoji="💭"),
    NodeNames.REASON: NodeMeta(
        label="Анализ и рассуждение",
        description="Генерация мыслей и анализ вопроса пользователя",
        emoji="🧠"
    ),
    NodeNames.FIRST_STEP: NodeMeta(
        label="Определение первого шага",
        description="Выбор начального действия для обработки запроса",
        emoji="🚦"
    ),
    NodeNames.SEARCH: NodeMeta(
        label="Веб-поиск",
        description="Поиск информации в интернете",
        emoji="🔍"
    ),
    NodeNames.RAG: NodeMeta(
        label="Поиск по базе знаний",
        description="Поиск во внутренних документах и базах данных",
        emoji="📚"
    ),
    NodeNames.WRITE: NodeMeta(
        label="Генерация ответа",
        description="Создание черновика ответа пользователю",
        emoji="✍️"
    ),
    NodeNames.FINALIZE: NodeMeta(
        label="Финальный ответ",
        description="Подготовка и выдача окончательного ответа",
        emoji="✅"
    ),
    NodeNames.CRITIQUE: NodeMeta(
        label="Критический анализ",
        description="Проверка и улучшение сгенерированного ответа",
        emoji="🔎"
    )
}
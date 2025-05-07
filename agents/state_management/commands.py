from enum import Enum
from typing import TypedDict, NamedTuple, Dict

class NodeMeta(NamedTuple):
    label: str  # Человекочитаемое название
    description: str  # Описание назначения ноды
    emoji: str = ""  # Опциональная иконка

class NodeNames(str, Enum):
    """Все зарегистрированные ноды в системе"""
    REASON = "reason"
    FIRST_STEP = "first_step"
    SEARCH = "search"
    RAG = "rag"
    WRITE = "write"
    FINALIZE = "finalize"
    CRITIQUE = "critique"

    @property
    def meta(self) -> NodeMeta:
        return NODE_METADATA[self]

class Command(TypedDict):
    """Структура команды перехода между нодами"""
    update: dict  # Обновления для состояния
    goto: NodeNames  # Следующая нода для выполнения

# Регистрируем метаданные отдельно от логики
NODE_METADATA: Dict[NodeNames, NodeMeta] = {
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
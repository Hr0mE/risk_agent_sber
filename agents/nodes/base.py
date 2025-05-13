from abc import ABC, abstractmethod
from typing import Dict, Any
from langgraph.graph import MessagesState
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig

import logging

#TODO вынести логгирование отдельным модулем
logger = logging.getLogger(__name__)

class BaseNode(ABC):
    """Абстрактный базовый класс для всех нод агента.
    
    Наследники должны реализовать:
    1. Метод execute() с логикой обработки состояния
    2. Собственные промпты и шаблоны при необходимости
    3. Валидацию входных/выходных данных
    
    Пример использования:
    class MyNode(BaseNode):
        def execute(self, state: MessagesState) -> Dict[str, Any]:
            # Логика обработки состояния
            return Command(
                update={"new_key": "value"},
                goto=NodeNames.SOMENAME
            )
    """

    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self._validate_dependencies()

    def _validate_dependencies(self): #TODO добавить проекрку на наличие моделей/инструментов
        """Проверка необходимых ReasoningState при инициализации"""
        pass

    def get_name(self) -> str:
        "Возвращает имя ноды"
        if not self.name:
            raise NotImplementedError(f"Имя ноды {self} не определено")
        return self.name

    @abstractmethod
    def execute(self, state: MessagesState, config: RunnableConfig = None) -> Command:
        """Основной метод обработки состояния.
        
        Args:
            state: Текущее состояние рассуждений агента
            
        Returns:
            Словарь с обновлениями для состояния
        """
        pass

    def __call__(self, state: MessagesState) -> Command:
        """Альтернативный интерфейс для выполнения ноды"""
        logger.debug(f"Executing node: {self.name}")
        return self.execute(state)

    def __repr__(self) ->  str:
        return f"<{self.__class__.__name__} '{self.name}'>"
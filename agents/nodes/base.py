from abc import ABC, abstractmethod
from typing import Dict, Any
from agents.state_management.reasoning_state import ReasoningState
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
        def execute(self, state: ReasoningState) -> Dict[str, Any]:
            # Логика обработки состояния
            return {"new_key": "value"}
    """

    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self._validate_dependencies()

    def _validate_dependencies(self): #TODO добавить проекрку на наличие моделей/инструментов
        """Проверка необходимых зависимостей при инициализации"""
        pass

    @abstractmethod
    def execute(self, state: ReasoningState) -> Dict[str, Any]:
        """Основной метод обработки состояния.
        
        Args:
            state: Текущее состояние рассуждений агента
            
        Returns:
            Словарь с обновлениями для состояния
        """
        pass

    def __call__(self, state: ReasoningState) -> Dict[str, Any]:
        """Альтернативный интерфейс для выполнения ноды"""
        logger.debug(f"Executing node: {self.name}")
        return self.execute(state)

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"
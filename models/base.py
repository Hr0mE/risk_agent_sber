import os
from abc import ABC, abstractmethod
from .config.base import BaseModelConfig, BaseAPIConfig
from typing import List

class BaseModel(ABC):
    """Абстрактный интерфейс модели"""
    def __init__(self, config: BaseModelConfig):
        self.config = config
        self._validate()
        self._initialize()

    @abstractmethod
    def _validate(self):
        """Валидация конфигурации"""
        pass

    @abstractmethod
    def _initialize(self):
        """Инициализация модели"""
        pass

    @abstractmethod
    def invoke(self, prompt: str) -> str:
        """Генерация ответа"""
        pass


class BaseAPIModel(BaseModel):
    """Базовый класс для API моделей через LangChain"""
    def __init__(self, config: BaseAPIConfig):
        super().__init__(config)

    def _validate(self):
        """Базовая валидация API ключа"""
        if self.config.api_key_env:
            self.config.api_key = os.getenv(self.config.api_key_env)
        if self.config.api_key:
            pass
        else:
            raise ValueError("API key is required")
    
    @abstractmethod
    def _initialize(self):
        """Инициализация модели. В наследниках должно быть определено self.model"""
        pass

    def invoke(self, prompt: str) -> str:
        try:
            result = self.model.invoke(prompt)
            return result.content
        except Exception as e:
            raise RuntimeError(f"Generation failed: {str(e)}")
        
    def __call__(self, prompt: str):
        return self.invoke(prompt)

class BaseAPIEmbedModel(BaseModel):
    """Базовый класс для API моделей через LangChain"""
    def __init__(self, config: BaseAPIConfig):
        super().__init__(config)

    def _validate(self):
        """Базовая валидация API ключа"""
        if self.config.api_key_env:
            self.config.api_key = os.getenv(self.config.api_key_env)
        if self.config.api_key:
            pass
        else:
            raise ValueError("API key is required")
    
    @abstractmethod
    def _initialize(self):
        """Инициализация модели. В наследниках должно быть определено self.model"""
        pass

    def embed_documents(self, documents: List[str]) -> List[List[str]]:
        return self.model.embed_documents(documents)
    
    def invoke(self, query: str) -> str:
        try:
            return self.model.embed_query(query)
        except Exception as e:
            raise RuntimeError(f"Embedding proccess failed: {str(e)}")
    
    def __call__(self, query: str):
        return self.invoke(query)
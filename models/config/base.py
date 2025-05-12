from pydantic import Field
from abc import ABC
from typing import Optional, Union

class BaseModelConfig(ABC):
    """Абстрактная базовая конфигурация"""
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = Field(30, description="Таймаут запроса в секундах")
    safe_mode: bool = Field(False, description="Включить безопасный режим")
    random_seed: Union[int, None] = Field(None, description="Сид для генерации")

    class Config:
        env_prefix = "LLM_"
        case_sensitive = False


class BaseAPIConfig(BaseModelConfig):
    """Базовый конфиг для API моделей"""
    api_key: Optional[str] = None
    api_key_env: Optional[str] = None
    api_base: str = Field(..., description="Базовый URL API")


class BaseLocalConfig(BaseModelConfig):
    """Базовый конфиг для локальных моделей"""
    base_url: str
    model_path: Optional[str] = Field(None, description="Путь к модели")
#models/config/base.py
from abc import ABC
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class BaseModelConfig(BaseSettings, ABC):
    """Абстрактная базовая конфигурация"""
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = Field(30, description="Request timeout in seconds")
    safe_mode: bool = Field(False, description="Enable safe mode")
    random_seed: int | None = Field(None, description="Random seed")

    class Config:
        env_prefix = "LLM_"
        case_sensitive = False

class BaseAPIConfig(BaseModelConfig):
    """Базовый конфиг для API моделей"""
    api_key: Optional[str] = None
    api_key_env: Optional[str] = None
    api_base: str = Field(description="Base API URL")

class BaseLocalConfig(BaseModelConfig):
    """Базовый конфиг для локальных моделей"""
    base_url: str
    model_path: Optional[str] = None

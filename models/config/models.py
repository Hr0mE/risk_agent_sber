# models/config/models.py
from .base import BaseAPIConfig, BaseLocalConfig


class OpenAIConfig(BaseAPIConfig):
    model_name: str = "gpt-3.5-turbo"
    api_key_env: str = "OPENAI_API_KEY"
    api_base: str = "https://api.openai.com/v1"


class MistralLargeAPIConfig(BaseAPIConfig):
    model_name: str = "mistral-large-2407"
    api_key_env: str = "MISTRAL_API_KEY"
    api_base: str = "https://api.mistral.ai/v1"


class MistralEmbedAPIConfig(BaseAPIConfig):
    model_name: str = "mistral-embed"
    api_key_env: str = "MISTRAL_API_KEY"
    api_base: str = "https://api.mistral.ai/v1"


class NomicEmbedAPIConfig(BaseAPIConfig):
    model_name: str = "nomic-embed-text-v1.5"
    api_key_env: str = "NOMIC_API_KEY"
    api_base: str = "https://api-atlas.nomic.ai/v1"


class LocalLlamaConfig(BaseLocalConfig):
    model_name: str = "llama-2-7b"
    base_url: str = "http://localhost:8080"

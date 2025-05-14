from huggingface_hub.hf_api import HfFolder
from dotenv import load_dotenv, dotenv_values
import os
from typing import List
from pathlib import Path

def load_environment(base_path : str = None, type_env: str = "dev") -> List:
    """Загрузка переменных окружения в зависимости от среды"""
    if not base_path:
        base_path = Path(__file__).resolve().parent / "env"

    env_file = f"{base_path}/{type_env}.env"

    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
    else:
        print(f"Warning: {env_file} not found, using system environment variables")
    
    return dotenv_values(env_file).keys()

def validate_environment() -> None:
    required_vars = ["HF_TOKEN", "MISTRAL_API_KEY", 'TAVILY_API_KEY', 'REDIS_URL']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required env vars: {missing}")

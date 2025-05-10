from dotenv import load_dotenv
import os

def load_environment():
    """Загрузка переменных окружения в зависимости от среды"""
    env = os.getenv("APP_ENV", "dev")
    env_file = f"./config/env/{env}.env"
    
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
    else:
        print(f"Warning: {env_file} not found, using system environment variables")

def validate_environment():
    required_vars = ["HF_TOKEN", "MISTRAL_API_KEY", 'TAVILY_API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required env vars: {missing}")
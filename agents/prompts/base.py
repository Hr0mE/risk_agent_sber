from langchain.prompts import ChatPromptTemplate
from pathlib import Path
from typing import Type, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, ValidationError
import logging

#TODO вынести логгирование отдельным модулем
logger = logging.getLogger(__name__)

class PromptTemplateConfig(BaseModel):
    """Конфигурация для валидации промптов"""
    required_vars: list[str]
    description: Optional[str] = None

class PromptManager:
    def __init__(self, templates_dir: str = None):
        if not templates_dir:
            self.templates_dir = Path(__file__).resolve().parent

        self.env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self._cache: Dict[str, Any] = {}
        
    def _get_template(self, path: str) -> Any:
        """Получение шаблона с кэшированием"""
        if path not in self._cache:
            self._cache[path] = self.env.get_template(path)
        return self._cache[path]

    def _validate_variables(self, variables: Dict, config: Type[PromptTemplateConfig]):
        """Валидация входных переменных через Pydantic"""
        config.model_validate(variables)
    

    def render(
        self,
        template_path: str, # Путь задаётся относительно самого base.py
        variables: Dict[str, Any],
        config: Type[PromptTemplateConfig] = None
    ) -> str:
        """Рендеринг промпта с валидацией"""
        try:
            template = self._get_template(template_path)
            
            if config:
                self._validate_variables(variables, config)
                
            return template.render(**variables)
        
        except ValidationError as ve:
            logger.error(f"Prompt validation error: {ve}")
            raise
        except Exception as e:
            logger.error(f"Error rendering template {template_path}: {e}")
            raise

    def create_chat_raw_prompt(self, template_path: str) -> ChatPromptTemplate:
        """Создание незаполненного шаблона под промпт"""
        raw_template = self.render(template_path, {})
        return ChatPromptTemplate.from_template(raw_template)


# Пример использования в ноде рассуждения
#class ReasonPromptConfig(PromptTemplateConfig):
#    required_vars = ["user_question", "history"]

# Пример конфига для промпта system/agent_identity.j2
#class AgentIdentityConfig(PromptTemplateConfig):
#    required_vars = ["tone", "expertise_area"]
from .manner_model import MannerInfo
from pydantic import BaseModel, Field
from typing import List

class ExtractorOutput(BaseModel):
  """Ожидаемый вывод из экстактора манеры"""
  is_to_memory: bool = Field(default=False, description="Надо сохранить манеру в память?")
  manner: MannerInfo

class FAQItem(BaseModel):
  """Элемент массива часто задаваемых вопросов"""
  theme: str
  questions: List[str]

class FAQExtractorOutput(BaseModel):
  """Ожидаемый вывод из экстрактора вопросов"""
  items: List[FAQItem]
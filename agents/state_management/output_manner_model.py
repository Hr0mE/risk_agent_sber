from .manner_model import MannerInfo
from pydantic import BaseModel, Field

class ExtractorOutput(BaseModel):
  """Ожидаемый вывод из экстактора манеры"""
  is_to_memory: bool = Field(default=False, description="Надо сохранить манеру в память?")
  manner: MannerInfo
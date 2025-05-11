from pydantic import BaseModel
from typing import List

class FAQItem(BaseModel):
  """Элемент массива часто задаваемых вопросов"""
  theme: str
  questions: List[str]
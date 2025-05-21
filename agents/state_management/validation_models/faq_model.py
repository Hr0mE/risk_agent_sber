from pydantic import BaseModel
from datetime import datetime
from typing import List


class Question(BaseModel):
    text: str
    score: float = 1.0
    send_date: datetime


class Theme(BaseModel):
    text: str
    score: float = 1.0


class FAQData(BaseModel):
    theme: Theme
    questions: List[Question]

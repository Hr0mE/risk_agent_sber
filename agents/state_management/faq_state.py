from langgraph.graph import MessagesState
from typing import List, Dict

class FAQState(MessagesState):
  question: str  # Вопрос пользователя из think
  raw_questions: List[str]  # Все вопросы пользователя
  faq: List[Dict[str, List[str]]]
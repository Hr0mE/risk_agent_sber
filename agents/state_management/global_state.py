from typing import Dict, List
from langgraph.graph import MessagesState
from .validation_models import MannerInfo

class GlobalState(MessagesState):
  problem_solving_question: str # Вопрос из ноды QuestionDecomposition, который поможет решить проблему пользователя
  sub_questions: List[str] # Подвопросы из ноды QuestionDecomposition
  last_reason: str
  user_question: str
  last_answer: str
  critique: List[str]
  final_decision: str
  final_answer: str
  search_query: str
  search_results: Dict
  rag_query: str
  rag_results: Dict

  is_info_in_memory: bool  # Есть ли манера в памяти
  is_write_to_memory: bool  # Надо ли записывать манеру в память
  manner: MannerInfo  # Данные о манере
  remaining_steps_to_check_manner: int  # Подсчет кол-ва шагов для адаптации
  raw_questions: List[str]  # Буфер вопросов для извлечения
  faq: List[Dict[str, List[str]]]  # Извлеченные часто задаваемые вопросы, сгруппированые по тематикам
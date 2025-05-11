from typing import Dict, List
from langgraph.graph import MessagesState
from .manner_model import MannerInfo

class ReasoningState(MessagesState):
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

  is_info_in_memory: bool
  manner: MannerInfo
  remaining_steps_to_check_manner: int
  # question: str  # TODO: поменять в faq на user_question
  raw_questions: List[str]
  faq: List[Dict[str, List[str]]]
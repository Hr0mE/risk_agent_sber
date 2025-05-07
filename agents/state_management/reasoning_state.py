from typing import Dict, List
from langgraph.graph import MessagesState

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
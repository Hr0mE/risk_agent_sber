from agents.nodes.base import BaseNode
from agents.state_management import (
    NodeNames,
    GlobalState
)
from langgraph.types import Command


class StoreQuestionNode(BaseNode):
  def __init__(self):
    super().__init__(name=NodeNames.STORE_QUESTION.value)

  def execute(self, state: GlobalState):
    question = state.get("problem_solving_question")
    if question:
        return Command(update={"raw_questions": state.get("raw_questions", []) + [question]})

    return Command()

from agents.nodes.base import BaseNode
from agents.state_management import (
    Command,
    NodeNames,
)
from langgraph.graph import MessagesState


class StoreQuestionNode(BaseNode):
  def __init__(self):
    super().__init__(name=NodeNames.STORE_QUESTION.value)

  def execute(self, state: MessagesState):
    question = state.get("user_question")
    if question:
        return Command(update={"raw_questions": state.get("raw_questions", []) + [question]})

    return Command()

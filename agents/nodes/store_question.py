from datetime import datetime
from agents.nodes.base import BaseNode
from agents.state_management import NodeNames, GlobalState
from agents.state_management.validation_models import Question
from langgraph.types import Command
from langchain_core.messages import HumanMessage


class StoreQuestionNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.STORE_QUESTION.value)

    def execute(self, state: GlobalState):
        # question = state.get("problem_solving_question")
        question = [m for m in state.get("messages") if isinstance(m, HumanMessage)][-1]
        question_to_store = Question(text=question.content, send_date=datetime.now())
        if question:
            return Command(update={"raw_questions": state.get("raw_questions", []) + [question_to_store]})

        return Command()

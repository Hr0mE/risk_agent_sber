from langgraph.types import Command
from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import (
    GlobalState, 
    NodeNames
)

from agents.state_management import QuestionDecompositionModel as output_model
from langchain_core.output_parsers import PydanticOutputParser
from models import MistralLargeModel as model
from models.config import MistralLargeAPIConfig as model_config


class QuestionDecompositionNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.QUESTION_DECOMPOSITION.value)
        self.parser = PydanticOutputParser(pydantic_object=output_model)
        self.prompt_manager = PromptManager()
        self.prompt_template = 'system/question_decomposition.j2'

        self.model = model(config=model_config())

    def execute(self, state: GlobalState) -> dict:
        prompt = self.prompt_manager.create_chat_raw_prompt(
            self.prompt_template
        )
        self.chain = prompt | self.model | self.parser
        
        # Выполнение цепочки обработки
        result = self.chain.invoke({
            "user_question": state.get("user_question", ""),
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return Command(
            update={
                "problem_solving_question": result.problem_solving_question,
                "sub_questions": result.sub_questions
            }
        )
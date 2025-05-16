from langgraph.types import Command
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from agents.nodes.base import BaseNode
from agents.state_management import (
    GlobalState, 
    NodeNames
)
from agents.state_management import CritiqueDecisionModel

from models import MistralLargeModel as model
from models.config import MistralLargeAPIConfig as model_config

from agents.prompts.base import PromptManager
from agents.edges.conditions import ConditionHandler

class CritiqueNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.CRITIQUE.value)
        self.parser = PydanticOutputParser(pydantic_object=CritiqueDecisionModel)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/critique.j2"
        self.model = model(config=model_config())
        
    
    
    def execute(self, state: GlobalState) -> Command:
        prompt = self.prompt_manager.create_chat_raw_prompt(self.prompt_template)
        chain = prompt | self.model | self.parser
        
        result = chain.invoke({
            "user_question": state.get("user_question", ""),
            "last_reason": state.get("last_reason", ""),
            "last_answer": state.get("last_answer", ""),
            "old_critique": state.get("critique", ""),
            "search_results": state.get("search_results", {}),
            "rag_results": state.get("rag_results", {}),
            "format_instructions": self.parser.get_format_instructions()

        })
                
        return Command(
            update={
                "final_decision": result.final_decision,
                "search_query": result.search_query,
                "rag_query": result.rag_query,
                "old_critique": result.critique
            },
            goto = ConditionHandler.evaluate_transition(
                source_node=self.name,
                result=result
            )
        )
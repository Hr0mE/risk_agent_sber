from typing import Optional
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from agents.nodes.base import BaseNode
from agents.state_management import (
    ReasoningState, 
    Command,
    NodeNames
)
from agents.state_management.critique_model import CritiqueDecisionModel
from models import MistralLargeModel as model
from agents.prompts.base import PromptManager
from agents.edges.conditions import ConditionHandler
import time

class CritiqueNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.CRITIQUE.value)
        self.parser = PydanticOutputParser(pydantic_object=CritiqueDecisionModel)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/critique.j2"
    
    
    def execute(self, state: ReasoningState) -> dict:
        # Потому что мистраль выдаёт 429 ошибку при частых запросах
        time.sleep(1)

        # Рендеринг промпта
        template = self.prompt_manager.render(
            self.prompt_template,
            {
                "format_instructions": self.parser.get_format_instructions()
            }
        )
        
        prompt = ChatPromptTemplate.from_messages([("system", template)])
        chain = prompt | model | self.parser
        
        result = chain.invoke({
            "user_question": state.user_question,
            "last_reason": state.last_reason
        })
                
        return Command(
            update={
                "final_decision": result.final_decision,
                "search_query": result.search_query,
                "rag_query": result.rag_query,
            },
            goto = ConditionHandler.evaluate_transition(
                source_node=self.name,
                result=result
            )
        )
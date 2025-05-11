from typing import Optional
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
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

class CritiqueNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.CRITIQUE.value)
        self.parser = PydanticOutputParser(pydantic_object=CritiqueDecisionModel)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/critique.j2"
    
    
    def execute(self, state: ReasoningState) -> Command:
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
            "last_reason": state.last_reason,
            "last_answer": state.last_answer,
            "old_critique": state.critique,
            "search_results": state.search_results,
            "rag_results": state.rag_results
        })
                
        return Command(
            update={
                "final_decision": result.final_decision,
                "search_query": result.search_query,
                "rag_query": result.rag_query,
                "critique": result.critique,
            },
            goto = ConditionHandler.evaluate_transition(
                source_node=self.name,
                result=result
            )
        )
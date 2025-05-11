from typing import Optional
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.nodes.base import BaseNode
from agents.state_management import (
    ReasoningState, 
    Command,
    NodeNames
)
from models import MistralLargeModel as model
from agents.prompts.base import PromptManager
from agents.edges.conditions import ConditionHandler

class WriteNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.WRITE.value)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/write.j2"
        
    
    def execute(self, state: ReasoningState) -> dict:
        prompt = self.prompt_manager.create_chat_raw_prompt(self.prompt_template)
        chain = prompt | model | StrOutputParser()
        
        result = chain.invoke({
                "user_question": state.user_question,
                "last_reason": state.last_reason,
                "search_results": state.search_results,
                "rag_results": state.rag_results
            })
                
        return Command(
            update={
                "last_answer": result
            }
        )
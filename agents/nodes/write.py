from typing import Optional
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.nodes.base import BaseNode
from agents.state_management import (
    ReasoningState, 
    Command,
    NodeNames
)
from agents.state_management.first_step_model import FirstStepDecision
from config.model_config import model
from agents.prompts.base import PromptManager
from agents.edges.conditions import ConditionHandler
import time

class WriteNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.WRITE)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/write.j2"
        
    
    def execute(self, state: ReasoningState) -> dict:
        # Потому что мистраль выдаёт 429 ошибку при частых запросах
        time.sleep(1)

        # Рендеринг промпта
        
        prompt = self.prompt_manager.create_chat_raw_prompt(self.prompt_template)
        chain = prompt | model | StrOutputParser()
        
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
from langchain_core.output_parsers import StrOutputParser
from agents.nodes.base import BaseNode
from agents.state_management import (
    GlobalState, 
    Command,
    NodeNames
)
from langgraph.graph import MessagesState
from models import MistralLargeModel as model
from agents.prompts.base import PromptManager
from models.config import MistralLargeAPIConfig as model_config


class WriteNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.WRITE.value)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/write.j2"
        self.model = model(config=model_config())

        
    
    def execute(self, state: GlobalState) -> dict:
        prompt = self.prompt_manager.create_chat_raw_prompt(self.prompt_template)
        chain = prompt | self.model | StrOutputParser()
        
        result = chain.invoke({
            "user_question": state.get("user_question", ""),
            "last_reason": state.get("last_reason", ""),
            "search_results": state.get("search_results", {}),
            "rag_results": state.get("rag_results", {})
        })
                
        return Command(
            update={
                "last_answer": result
            }
        )
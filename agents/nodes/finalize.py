from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import (
    ReasoningState, 
    NodeNames,
    Command
)
from agents.state_management.reasoning_state import ReasoningState
from langchain_core.output_parsers import StrOutputParser
from models import MistralLargeModel as model
import time # Нужен для создания задержки из-за ограничения в кол-во запросов к модели


class FinalizeNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.REASON.value)
        
        self.prompt_manager = PromptManager()
        self.prompt_template = 'system/finalize.j2'
        
        #TODO сделать проверку через конфиг
        #self.config = FinalizePromptConfig

    def execute(self, state: ReasoningState) -> dict:
        prompt = self.prompt_manager.create_chat_raw_prompt(
            self.prompt_template
        )
        self.chain = prompt | model | StrOutputParser()
        
        # Выполнение цепочки обработки
        result = self.chain.invoke({
            "user_question": state.user_question,
            "last_reason": state.last_reason,
            "critique": state.critique,
            "last_answer": state.last_answer,
            "search_results": state.search_results,
            "rag_results": state.rag_results,
        })

        # Возвращаем обновления для состояния
        return Command(
            update={"final_answer": result}
        )
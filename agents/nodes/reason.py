# agents/nodes/think.py
from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import (
    ReasoningState, 
    NodeNames
)
from agents.state_management.reasoning_state import ReasoningState
from langchain_core.output_parsers import StrOutputParser
from models import MistralLargeModel as model
import time # Нужен для создания задержки из-за ограничения в кол-во запросов к модели


class ReasonNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.REASON.value)
        
        self.prompt_manager = PromptManager()
        self.prompt_template = 'system/reason.j2'
        #TODO сделать проверку через конфиг
        #self.config = ReasonPromptConfig

    def execute(self, state: ReasoningState) -> dict:
        # Потому что мистраль выдаёт 429 ошибку при частых запросах
        time.sleep(1)

        prompt = self.prompt_manager.create_chat_raw_prompt(
            self.prompt_template
        )
        self.chain = prompt | model | StrOutputParser()
        
        # Выполнение цепочки обработки
        result = self.chain.invoke({
            "user_question": state.user_question,
        })

        # Возвращаем обновления для состояния
        return {
            "lasr_reason": result
        }
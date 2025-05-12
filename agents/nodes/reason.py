from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import (
    GlobalState, 
    NodeNames,
    Command
)
from langchain_core.output_parsers import StrOutputParser
from models import MistralLargeModel as model


class ReasonNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.REASON.value)
        
        self.prompt_manager = PromptManager()
        self.prompt_template = 'system/reason.j2'
        #TODO сделать конфиг для модели
        self.model = model #model(config=ModelConfig)
        #TODO сделать проверку через конфиг
        #self.config = ReasonPromptConfig

    def execute(self, state: GlobalState) -> dict:
        prompt = self.prompt_manager.create_chat_raw_prompt(
            self.prompt_template
        )
        self.chain = prompt | self.model | StrOutputParser()
        
        # Выполнение цепочки обработки
        result = self.chain.invoke({
            "user_question": state.get("user_question", ""),
        })

        # Возвращаем обновления для состояния
        return Command(
            update={"last_reason": result}
        )
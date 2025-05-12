from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import (
    GlobalState, 
    NodeNames,
    Command
)
from langchain_core.output_parsers import StrOutputParser
from models import MistralLargeModel as model
from models.config import MistralLargeAPIConfig as model_config


class FinalizeNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.FINALIZE.value)
        
        self.model = model(config=model_config())


        self.prompt_manager = PromptManager()
        self.prompt_template = 'system/finalize.j2'
        
        #TODO сделать проверку через конфиг
        #self.prompt_config = FinalizePromptConfig

    def execute(self, state: GlobalState) -> dict:
        prompt = self.prompt_manager.create_chat_raw_prompt(
            self.prompt_template
        )
        self.chain = prompt | self.model | StrOutputParser()
        
        # Выполнение цепочки обработки
        result = self.chain.invoke({
            "user_question": state.get("user_question", ""),
            "last_reason": state.get("last_reason", ""),
            "critique": state.get("critique", ""),
            "last_answer": state.get("last_answer", ""),
            "search_results": state.get("search_results", {}),
            "rag_results": state.get("rag_results", {}),
        })

        # Возвращаем обновления для состояния
        return Command(
            update={"final_answer": result}
        )
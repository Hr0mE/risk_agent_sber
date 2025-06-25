import os
from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import NodeNames, GlobalState
from langchain.prompts import ChatPromptTemplate
from models import MistralLargeModel as model
from langchain_core.output_parsers import JsonOutputParser
from agents.state_management import ExtractorOutput
from langchain_core.messages import HumanMessage
from models.config import MistralLargeAPIConfig as model_config

from langgraph.types import Command


class MannerExtractNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.EXTRACT_MANNER.value)
        self.parser = JsonOutputParser(pydantic_object=ExtractorOutput)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/manner_extract.j2"
        self.model = model(config=model_config())

    def execute(self, state: GlobalState):
        # Если в памяти что-то есть и не пришла пора извлекать манеру(адаптироваться),
        #  то не извлекаем ее(уменьшаем шаги на 1)
        if state.get("is_info_in_memory", False) and state.get("remaining_steps_to_check_manner", -1) != 0:
            return Command(
                update={
                    "is_write_to_memory": False,
                    "remaining_steps_to_check_manner": state["remaining_steps_to_check_manner"] - 1,
                }
            )

        messages = state["messages"]  # Извлекаем ВСЕ сообщения чата

        last_n_human_messages = [m for m in messages if isinstance(m, HumanMessage)][
            -int(os.getenv("MESSAGES_TO_ANALIZE", 3)) :
        ]  # Получаем n последних сообщений ПОЛЬЗОВАТЕЛЯ
        messages_for_prompt = "\n".join(
            [f"{i + 1}. {message}" for i, message in enumerate(last_n_human_messages)]
        )  # Формируем данные в промпт

        template = self.prompt_manager.render(self.prompt_template, {})
        prompt = ChatPromptTemplate.from_messages([("system", template)])

        chain = prompt | self.model | self.parser

        result = chain.invoke(
            {
                "format_instructions": self.parser.get_format_instructions(),
                "query": messages_for_prompt,
            }
        )

        if result["is_to_memory"]:
            return Command(
                update={
                    "is_write_to_memory": result["is_to_memory"],
                    "remaining_steps_to_check_manner": int(os.getenv("STEPS_TO_CHECK", 3)),
                    "manner": result["manner"],
                }
            )

        return Command()

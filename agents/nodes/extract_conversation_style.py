import os
from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import (
    Command,
    NodeNames,
)
from langchain.prompts import ChatPromptTemplate
from models import MistralLargeModel as model
from langchain_core.output_parsers import JsonOutputParser
from agents.state_management import ExtractorOutput
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState


class MannerExtractNode(BaseNode):
  def __init__(self, name = None):
    super().__init__(name=NodeNames.EXTRACT_MANNER.value)
    self.parser = JsonOutputParser(pydantic_object=ExtractorOutput)
    self.prompt_manager = PromptManager()
    self.prompt_template = "system/manner_extract.j2"

  def execute(self, state: MessagesState, config: RunnableConfig):
    # Если в памяти что-то есть и не пришла пора извлекать манеру, то не извлекаем ее(уменьшаем шаги на 1)
    if state.get("is_info_in_memory", False) and state.get("remaining_steps_to_check_manner", -1) != 0:
      return Command(
        update={
          "remaining_steps_to_check_manner": state["remaining_steps_to_check_manner"] - 1,
        }
      ) 
    
    messages = state["messages"]  # Извлекаем ВСЕ сообщения чата
    
    last_n_human_messages = [m for m in messages if isinstance(m, HumanMessage)][-os.getenv("MESSAGES_TO_ANALIZE", 3):]  # Получаем все сообщения ПОЛЬЗОВАТЕЛЯ
    messages_for_prompt = "\n".join([f"{i+1}. {message}" for i, message in enumerate(last_n_human_messages)])  # Берем n последних сообщения

    template = self.prompt_manager.render(
      self.prompt_template,
      {
        "format_instructions": self.parser.get_format_instructions()
      }
    )
    prompt = ChatPromptTemplate.from_messages([("system", template)])

    chain = prompt | model | self.parser

    result = chain.invoke({
      "query": messages_for_prompt,
    })

    if result["is_to_memory"]:
      return Command(
        update={
          "is_info_in_memory": result["is_to_memory"],
          "remaining_steps_to_check_manner": os.getenv("STEPS_TO_CHECK", 3),
          "manner": result["manner"],
        }
      )
    
    return Command(
      update={
        "is_info_in_memory": False,
      }
    )
from agents.nodes.base import BaseNode
from agents.state_management import (
    # Command,
    NodeNames,
    GlobalState
)
from langgraph.graph import MessagesState
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig
from utils.similarity_of_topics import find_similar_theme
from database import memory_store


class FAQWriteNode(BaseNode):
  def __init__(self):
    super().__init__(name=NodeNames.WRITE_FAQ.value)

  def execute(self, state: GlobalState, config: RunnableConfig):
    if not state.get("faq", []):
      return Command()
    
    user_uuid, memory_uuid = config["metadata"]["user_uuid"], config["metadata"]["memory_uuid"]

    namespace = ("user_info", user_uuid)
    curr_memory_data = memory_store.get(namespace, memory_uuid) or {}
    curr_val = curr_memory_data.value if curr_memory_data != {} else {} 
    memory_faq = curr_val.get('faq', None)

    # Если в памяти пусто, то записываем все FAQ, иначе дополняем память
    if memory_faq is None:
      curr_val["faq"] = state["faq"]
    else:
      memory_faq_temp = {i['theme']: i for i in memory_faq}
      state_faq = state['faq']

      for item in state_faq:
        theme, questions = item['theme'], item['questions']
        similar_theme = find_similar_theme(theme, memory_faq_temp.keys())

        if similar_theme:
          existing_questions = set(memory_faq_temp[similar_theme]['questions'])
          new_questions = [q for q in questions if q not in existing_questions]

          memory_faq_temp[similar_theme]['questions'].extend(new_questions)
        else:
          memory_faq.append(item)

      curr_val["faq"] = memory_faq


      memory_store.put(namespace, memory_uuid, curr_val)

      return Command(
        update={
          "faq": [],
        }
      )
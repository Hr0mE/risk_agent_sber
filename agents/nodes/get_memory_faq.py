from agents.nodes.base import BaseNode
from langchain_core.runnables import RunnableConfig
from agents.state_management import (
    Command,
    NodeNames
)
from database import memory_store
from langgraph.graph import MessagesState


class GetFAQFromMemoryNode(BaseNode):
  def __init__(self):
    super().__init__(name=NodeNames.GET_FAQ.value)

  def execute(self, state: MessagesState, config: RunnableConfig):
    user_uuid = config["metadata"]["user_uuid"]
    namespace = ("user_info", user_uuid)
    results = memory_store.search(namespace)

    memory_item = results[-1].dict() if results else None
    faq_list= memory_item["value"].get("faq", None) if memory_item else None

    if faq_list:
      return Command(
        update={
          "faq": faq_list
        }
      )
    
    return Command()
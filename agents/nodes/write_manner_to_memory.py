from agents.nodes.base import BaseNode
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from agents.state_management import (
    NodeNames,
    GlobalState
)
from database import memory_store

class WriteMannerToMemoryNode(BaseNode):
  def __init__(self):
    super().__init__(name=NodeNames.WRITE_MANNER.value)

  def execute(self, state: GlobalState, config: RunnableConfig):
    if state.get("is_write_to_memory", False):
      user_uuid, memory_uuid = config["configurable"]["metadata"]["user_uuid"], config["configurable"]["metadata"]["memory_uuid"]
      # user_uuid, memory_uuid = config["metadata"]["user_uuid"], config["metadata"]["memory_uuid"]

      namespace = ("user_info", user_uuid)

      curr_memory_data = memory_store.get(namespace, memory_uuid) or {}
      curr_val = curr_memory_data.value if curr_memory_data != {} else {} 
      curr_val["manner"] = state["manner"]
      memory_store.put(namespace, memory_uuid, curr_val)

      return Command(
        update={
          "is_info_in_memory": True
        }
      )
    
    return Command()
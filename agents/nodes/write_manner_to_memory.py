from agents.nodes.base import BaseNode
from langchain_core.runnables import RunnableConfig
from agents.state_management import (
    MannerState,
    Command
)


class WriteMannerToMemoryNode(BaseNode):
  def __init__(self, name = None):
    super().__init__(name)

  def execute(self, state: MannerState, config: RunnableConfig):
    if state.get("is_info_in_memory", False):
      user_uuid, memory_uuid = config["metadata"]["user_uuid"], config["metadata"]["memory_uuid"]

      namespace = ("user_info", user_uuid)

      curr_memory_data = memory_store.get(namespace, memory_uuid) or {}
      curr_val = curr_memory_data.value if curr_memory_data != {} else {} 
      curr_val["manner"] = state["manner"]
      memory_store.put(namespace, memory_uuid, curr_val)
    
    return Command()
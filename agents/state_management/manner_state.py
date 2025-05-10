from langgraph.graph import MessagesState
from .manner_model import MannerInfo

class MannerState(MessagesState):
  is_info_in_memory: bool
  manner: MannerInfo
  remaining_steps_to_check_manner: int
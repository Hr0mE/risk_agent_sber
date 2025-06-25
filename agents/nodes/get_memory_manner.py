from agents.nodes.base import BaseNode
from langchain_core.runnables import RunnableConfig
from agents.state_management import MannerInfo, NodeNames, GlobalState
from database import memory_store
from langgraph.types import Command


class GetMannerFromMemoryNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.GET_MANNER.value)

    def execute(self, state: GlobalState, config: RunnableConfig):
        user_uuid = config["configurable"]["metadata"]["user_uuid"]
        # user_uuid = config["metadata"]["user_uuid"]
        namespace = ("user_info", user_uuid)
        results = memory_store.search(namespace)

        memory_item = results[-1].dict() if results else None
        manner_item = memory_item["value"].get("manner", None) if memory_item else None
        manner = MannerInfo(**manner_item) if manner_item else None
        if manner:
            return Command(update={"manner": manner})

        return Command()

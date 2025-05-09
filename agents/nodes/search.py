from agents.nodes.base import BaseNode
from tavily import TavilyClient
from agents.state_management import (
    ReasoningState, 
    NodeNames,
    Command
)

class SearchNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.SEARCH.value)

    def execute(self, state: ReasoningState) -> dict:
        tavily_client = TavilyClient()
        response = tavily_client.search(state.search_query)
        result = state.get("search_results", {})
        result[state.search_query] = response
        return Command(
            update={"search_results": result}
        )
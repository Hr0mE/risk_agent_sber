from agents.nodes.base import BaseNode
from tavily import TavilyClient
from agents.state_management import (
    GlobalState, 
    NodeNames
)
from langgraph.types import Command

class SearchNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.SEARCH.value)

    def execute(self, state: GlobalState) -> dict:
        tavily_client = TavilyClient()
        
        search_query: str = state.get("search_query") 
        if not search_query:
            raise ValueError(f"Поле search_query в {state} ({type(state)}) не должно быть пустым")
        response = tavily_client.search(search_query)
        result = state.get("search_results", {})
        result[search_query] = response
        return Command(
            update={"search_results": result}
        )
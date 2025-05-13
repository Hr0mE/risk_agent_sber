from langgraph.graph import StateGraph
from typing import Dict
from langchain_core.runnables import RunnableConfig

# from agents.chains import OnlySearchChain as chain
from agents.chains import FullExecutionChain as chain
#from agents.chains import OnlyMemoryChain as chain
from agents.state_management import GlobalState as state
from config import load_environment, validate_environment
import asyncio


class BaseAgent:
    def __init__(self, inputs: Dict[str, str] = None, config: RunnableConfig = None):
        self.inputs = inputs
        self.config = config
        self.graph = chain().build(state)

    async def run(self) -> StateGraph:
        if not self.inputs:
            raise ValueError("inputs не должен быть пустым!")

        async for event in self.graph.astream_events(self.inputs, self.config, version="v2"):
            event_type = event.get('event', None)
            agent = event.get('name', '')
            if agent in ["_write", "RunnableSequence", "__start__", "__end__", "LangGraph"]:
                continue
            if event_type == 'on_chat_model_stream':
                print(event['data']['chunk'].content, end='')
            elif event_type == 'on_chain_start':
                print(f"<{agent}>")
            elif event_type == 'on_chain_end':
                print(f"</{agent}>")
            # else:
            #print(event)

async def main():
    load_environment()
    validate_environment()

    text = "Какие сроки установлены для представления головной кредитной организацией отчётов о расчёте операционного риска банковской группы в Банк России?"
    
    inputs = {
        "messages": text,
        "user_question": text,
    }

    config = {
        "thread_id": 69, 
        "user_uuid": "2722D3D2-AD19-4672-9B32-BA2221077262", 
        "memory_uuid": "2BD632C8-E4D5-456C-BEB0-025C2940D6E1",
    }
    
    await BaseAgent(inputs=inputs, config=config).run()
    

if __name__ == "__main__":
    asyncio.run(main())
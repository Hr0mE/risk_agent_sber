from langgraph.graph import StateGraph
from typing import Dict

from agents.chains import FullExecutionChain as chain
from agents.state_management import GlobalState as state
from config import load_environment, validate_environment
import asyncio


class BaseAgent:
    def __init__(self, inputs: Dict[str, str] = None):
        self.inputs = inputs
        self.graph = chain().build(state)

    async def run(self) -> StateGraph:
        if not self.inputs:
            raise ValueError("inputs не должен быть пустым!")

        async for event in self.graph.astream_events(self.inputs, version="v2"):
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

    
    inputs = {"user_question": "Какие сроки установлены для представления головной кредитной организацией отчётов о расчёте операционного риска банковской группы в Банк России?"}
    
    await BaseAgent(inputs=inputs).run()
    

if __name__ == "__main__":
    asyncio.run(main())
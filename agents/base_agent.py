import asyncio
from typing import Dict
from uuid import uuid4

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.types import Checkpointer

# from agents.chains import OnlySearchChain as chain
# from agents.chains import FullExecutionChain as chain
# from agents.chains import OnlyMemoryChain as chain
from agents.chains import RagChain as chain
from agents.state_management import GlobalState as state
from config import load_environment, validate_environment


class BaseAgent:
    def __init__(self, checkpointer: Checkpointer = None):
        self.graph = chain().build(
            state,
            name="Risk Agent by RD-ml team(отсылка на Роберта Дауни мл.)",
            checkpointer=checkpointer,
        )

    async def run(self, inputs: Dict[str, str], config: RunnableConfig = None) -> StateGraph:
        if not inputs:
            raise ValueError("inputs не должен быть пустым!")

        async for event in self.graph.astream_events(inputs, config, version="v2"):
            event_type = event.get("event", None)
            agent = event.get("name", "")
            if agent in ["_write", "RunnableSequence", "__start__", "__end__", "LangGraph"]:
                continue
            if event_type == "on_chat_model_stream":
                print(event["data"]["chunk"].content, end="")
            elif event_type == "on_chain_start":
                print(f"<{agent}>")
            elif event_type == "on_chain_end":
                print(f"</{agent}>")
            # else:
            # print(event)


async def main():
    load_environment()
    validate_environment()

    main_graph = BaseAgent(checkpointer=MemorySaver())

    user_uuid = str(uuid4())
    memory_uuid = str(uuid4())
    thread_id = str(uuid4())

    while True:
        text = input("\n\033[34mВведите сообщение:\033[37m ")
        if text.lower() in ["exit", "выход", "пока", "quit", "q", "esc"]:
            break

        inputs = {"messages": text, "user_question": text}
        config = {
            "thread_id": thread_id,
            "configurable": {
                "metadata": {
                    "user_uuid": user_uuid,
                    "memory_uuid": memory_uuid,
                }
            },
        }

        await main_graph.run(inputs=inputs, config=config)


if __name__ == "__main__":
    asyncio.run(main())

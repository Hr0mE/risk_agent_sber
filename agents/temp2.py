import asyncio
from typing import Dict

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.types import Checkpointer

#from agents.chains import OnlySearchChain as chain
from agents.chains import FullExecutionChain as chai1n

# from agents.chains import OnlyMemoryChainWithoutMannerExtract as chain

# from agents.chains import RagChain as chain
from agents.state_management import GlobalState as state
from agents.state_management.validation_models.manner_model import MannerInfo
from config import load_environment, validate_environment
from database import memory_store


class BaseAgent:
    def __init__(self, checkpointer: Checkpointer = None):
        self.graph = chain().build(
            state,
            name="Risk Agent by RD-ml team",
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

    graph = BaseAgent(checkpointer=MemorySaver())

    user_uuid = "CD8DE8A9-4AE0-4800-B2F1-692B2F46817F"
    memory_uuid = "50E6562C-7551-4E71-A1B7-8683DC494D85"

    while True:
        manner_1 = MannerInfo(
            tone="дружелюбный",
            emotionality="низкая",
            appeal="на ты",
            additionally=["использование сленга", "синтаксис: короткие предложения"],
        )

        manner_2 = MannerInfo(
            tone="нейтральный, сухой",
            emotionality="низкая",
            appeal="на вы",
            additionally=["длинные фразы", "использование терминов", "научный стиль"],
        )
        text = input(f"\nВыберите манеру: \n1. {manner_1.__repr__()}\n\n2. {manner_2.__repr__()}\nВыбор: ")

        match text.lower():
            case "1":
                manner = manner_1
            case "2":
                manner = manner_2
            case _:
                print("\nИспользуем первую манеру")
                manner = manner_1

        namespace = ("user_info", user_uuid)
        curr_memory_data = memory_store.get(namespace, memory_uuid) or {}
        curr_val = curr_memory_data.value if curr_memory_data != {} else {}
        curr_val["manner"] = manner.model_dump()
        memory_store.put(namespace, memory_uuid, curr_val)

        text = input("Введите сообщение: ")
        if text.lower() == "exit":
            break
        inputs = {"messages": text, "user_question": text}
        config = {
            "thread_id": 69,
            "configurable": {
                "metadata": {
                    "user_uuid": user_uuid,
                    "memory_uuid": memory_uuid,
                }
            },
        }

        await graph.run(inputs=inputs, config=config)


if __name__ == "__main__":
    asyncio.run(main())

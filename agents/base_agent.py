import asyncio
from typing import Dict
from uuid import uuid4

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph
from langgraph.types import Checkpointer

# from agents.chains import OnlySearchChain as chain
# from agents.chains import FullExecutionChain as chain
from agents.chains import OnlyMemoryChain as chain

# from agents.chains import RagChain as chain
from agents.state_management import GlobalState as state
from config import load_environment, validate_environment
from database import memory_store


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


def get_best_question(faq_list):
    max_theme_score = max(item["theme"]["score"] for item in faq_list)
    # Тематики с максимальным баллом
    top_themes = [item for item in faq_list if item["theme"]["score"] == max_theme_score]

    if len(top_themes) == 1:
        questions = top_themes[0]["questions"]
        best_question = max(questions, key=lambda q: q["score"])
        return best_question["text"]
    else:
        all_questions = []
        for theme in top_themes:
            all_questions.extend(theme["questions"])
        best_question = max(all_questions, key=lambda q: q["score"])
        return best_question["text"]


async def main():
    load_environment()
    validate_environment()

    main_graph = BaseAgent(checkpointer=MemorySaver())

    user_uuid = "CD8DE8A9-4AE0-4800-B2F1-692B2F46817F"
    memory_uuid = "50E6562C-7551-4E71-A1B7-8683DC494D85"
    # user_uuid = str(uuid4())
    # memory_uuid = str(uuid4())
    thread_id = str(uuid4())

    while True:
        # Примерная работа предложения вопроса
        is_new_thread = input("Новый чат?")
        count = 0
        if is_new_thread.lower() in ["y", "yeah", "yes"] and count == 0:
            namespace = ("user_info", user_uuid)
            curr_memory_data = memory_store.get(namespace, memory_uuid) or {}
            curr_val = curr_memory_data.value if curr_memory_data != {} else {}
            memory_faq = curr_val.get("faq", None)
            if memory_faq is not None:
                suggestion = get_best_question(memory_faq)
                print(f"\n\033[33mАссистент:\n  Хотитие, отвечу на вопрос:\033[37m {suggestion}")

        text = input("\n\033[34mВведите сообщение:\033[37m ")
        if text.lower() in ["exit", "выход", "пока", "quit", "q", "esc"]:
            break
        count += 1
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

import json
import math
from datetime import datetime

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from pydantic import RootModel

from agents.nodes.base import BaseNode
from agents.state_management import GlobalState, NodeNames
from database import memory_store
from utils.similarity_of_topics import find_similar_theme


class FAQWriteNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.WRITE_FAQ.value)

    def execute(self, state: GlobalState, config: RunnableConfig):
        if not state.get("is_write_faq", False):
            return Command()

        user_uuid = config["configurable"]["metadata"]["user_uuid"]
        memory_uuid = config["configurable"]["metadata"]["memory_uuid"]

        namespace = ("user_info", user_uuid)
        curr_memory_data = memory_store.get(namespace, memory_uuid) or {}
        curr_val = curr_memory_data.value if curr_memory_data != {} else {}
        memory_faq = curr_val.get("faq", None)

        state_faq = state["faq"]

        # Если в памяти пусто, то записываем все FAQ, иначе дополняем память
        if memory_faq is None:
            # Подсчет баллов тематик и вопросов
            for faq_item in state_faq:
                faq_item.theme.score += math.log(1 + len(faq_item.questions))
                for question in faq_item.questions:
                    now = datetime.now()
                    question.score *= math.exp(-3 * (now - question.send_date).total_seconds())

            curr_val["faq"] = json.loads(RootModel(state_faq).model_dump_json())
        else:
            # [
            #   {
            #     'theme': {
            #       'text': 'Аппетит к риску',
            #       'score': 1.6931471805599454
            #     },
            #     'questions': [
            #       {
            #         'text': 'Что такое аппетит к риску?',
            #         'score': 7.059341935886362e-09,
            #         'send_date': '2025-05-19T03:15:47.797530'
            #       }
            #     ]
            #   },
            #   {
            #     'theme': {
            #       'text': 'Чаевые',
            #       'score': 1.6931471805599454
            #     },
            #     'questions': [
            #       {
            #         'text': 'является ли факт принятия чаевых в размере 20 тыс руб событием оприска?',
            #         'score': 0.0003621804462607523,
            #         'send_date': '2025-05-19T03:15:53.220303'
            #       }
            #     ]
            #   }
            # ]
            memory_faq_temp = {i["theme"]["text"]: i for i in memory_faq}

            for faq_item in state_faq:
                theme_text = faq_item.theme.text
                questions = faq_item.questions

                faq_item.theme.score += math.log(1 + len(questions))
                now = datetime.now()
                for question in questions:
                    question.score *= math.exp(-3 * (now - question.send_date).total_seconds())

                similar_theme = find_similar_theme(theme_text, memory_faq_temp.keys())

                if similar_theme:
                    memory_faq_temp[similar_theme]["theme"]["score"] = (
                        memory_faq_temp[similar_theme]["theme"]["score"] + faq_item.theme.score
                    )

                    existing_questions_texts = {
                        q["text"] for q in memory_faq_temp[similar_theme]["questions"]
                    }
                    for q in questions:
                        if q.text not in existing_questions_texts:
                            memory_faq_temp[similar_theme]["questions"].append(
                                {"text": q.text, "score": q.score, "send_date": q.send_date.isoformat()}
                            )
                else:
                    memory_faq.append(json.loads(RootModel([faq_item]).model_dump_json())[0])

            curr_val["faq"] = list(memory_faq)

        memory_store.put(namespace, memory_uuid, curr_val)

        return Command(
            update={
                "faq": [],
            }
        )

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

    def _get_theme_score(self, len_theme_questions: int, k: int | float = 1) -> float:
        """Подсчет балла тематики. log2 не позволяет расти баллу линейно и большим при многом кол-ве вопросов

        Args:
            len_theme_questions (int): длина списка вопросов в тематике
            k (int | float, optional): коэффициент, чтобы не было 0. Defaults to 1.

        Returns:
            float: балл тематики
        """
        return math.log2(k + len_theme_questions)
    
    def _get_question_score(self, question_date: datetime, k: int | float = 0.05) -> float:
        """Подсчет балла вопроса. 
        Экспонента позволяет считать новые (последние заданные) вопросы более важными, чем прошлые.
        Коэффициент отвечает за быстроту устаревания вопросов, чем больше, тем быстрее.

        Args:
            question_date (datetime): дата отправки вопроса
            k (int | float, optional): коэффициент устаревания. Defaults to 0.05.

        Returns:
            float: балл вопроса
        """
        now = datetime.now()
        return math.exp(-k * (now - question_date).total_seconds())

    def execute(self, state: GlobalState, config: RunnableConfig):
        # Если не надо записывать ничего, то переходим к следующей ноде
        if not state.get("is_write_faq", False):
            return Command()

        # Получем необходимые переменные из агента(данные о пользователе и ячейке памяти)
        user_uuid = config["configurable"]["metadata"]["user_uuid"]
        memory_uuid = config["configurable"]["metadata"]["memory_uuid"]

        # Получем текущую хранимую информацию о пользователе из памяти
        namespace = ("user_info", user_uuid)
        curr_memory_data = memory_store.get(namespace, memory_uuid) or {}
        curr_val = curr_memory_data.value if curr_memory_data != {} else {}
        memory_faq = curr_val.get("faq", None)

        # Получаем извлеченные FAQ из графа
        state_faq = state["faq"]

        # Если в памяти пусто, то записываем все FAQ, иначе дополняем память
        if memory_faq is None:
            # Подсчет баллов тематик и вопросов для первой записи в память
            for faq_item in state_faq:
                faq_item.theme.score += self._get_theme_score(len(faq_item.questions))
                for question in faq_item.questions:
                    question.score *= self._get_question_score(question.send_date)

            curr_val["faq"] = json.loads(RootModel(state_faq).model_dump_json())
        else:
            # ПРИМЕР хранимой информации
            # [
            #   {
            #     'theme': {
            #       'text': 'Аппетит к риску',
            #       'score': 1.0
            #     },
            #     'questions': [
            #       {
            #         'text': 'Что такое аппетит к риску?',
            #         'score': 1.0,
            #         'send_date': '2025-05-19T03: 15: 47.797530'
            #       }
            #     ]
            #   },
            #   {
            #     'theme': {
            #       'text': 'Чаевые',
            #       'score': 1.0
            #     },
            #     'questions': [
            #       {
            #         'text': 'является ли факт принятия чаевых в размере 20 тыс руб событием оприска?',
            #         'score': 1.0,
            #         'send_date': '2025-05-19T03: 15: 53.220303'
            #       }
            #     ]
            #   }
            # ]

            # {
            #   "is_to_memory": true,
            #   "manner": {
            #     "tone": "неформальный, дружелюбный",
            #     "emotionality": "умеренная",
            #     "appeal": "на ты",
            #     "additionally": [
            #       "использует жаргон",
            #       "короткие предложения",
            #       "вопросы"
            #     ]
            #   }
            # }
            memory_faq_temp = {i["theme"]["text"]: i for i in memory_faq}

            # Подсчет баллов для существующих записей
            for faq_item in state_faq:
                theme_text = faq_item.theme.text
                questions = faq_item.questions

                # Благодаря данной формуле, рост количества баллов тематики 
                # не растет линейно от числа вопросов в ней, 
                # что дает замедление роста баллов тематики с увеличением числа вопросов 
                # (чем больше вопросов, тем медленнее увеличиваются баллы тематики). 
                # Также, подсчет среднего балла всех вопросов тематики позволяет тематике, 
                # где хранятся более важные вопросы, иметь больший итоговый балл.
                avg_question_score = sum(q.score for q in questions) / len(questions)
                faq_item.theme.score += self._get_theme_score(len(questions)) * avg_question_score

                for question in questions:
                    question.score *= self._get_question_score(question.send_date)

                similar_theme = find_similar_theme(theme_text, memory_faq_temp.keys())

                # Если есть тема в памяти, то меняем ее баллы, иначе просто дописываем
                if similar_theme:
                    memory_faq_temp[similar_theme]["theme"]["score"] = (
                        memory_faq_temp[similar_theme]["theme"]["score"] + faq_item.theme.score
                    )

                    existing_questions_texts = {
                        q["text"] for q in memory_faq_temp[similar_theme]["questions"]
                    }
                    for index, q in enumerate(questions):
                        if q.text not in existing_questions_texts:
                            memory_faq_temp[similar_theme]["questions"].append(
                                {"text": q.text, "score": q.score, "send_date": q.send_date.isoformat()}
                            )
                        else:
                            memory_faq_temp[similar_theme]["questions"][index][
                                "send_date"
                            ] = q.send_date.isoformat()
                else:
                    memory_faq.append(json.loads(RootModel([faq_item]).model_dump_json())[0])

            curr_val["faq"] = list(memory_faq)

        memory_store.put(namespace, memory_uuid, curr_val)

        return Command(
            update={
                "faq": [],
            }
        )

import os

from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langgraph.types import Command

from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import (
    FAQExtractorOutput,
    GlobalState,
    NodeNames,
)
from agents.state_management.validation_models import Question, Theme, FAQData
from models import MistralLargeModel as model
from models.config import MistralLargeAPIConfig as model_config


class FAQExtractNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.EXTRACT_FAQ.value)
        self.parser = JsonOutputParser(pydantic_object=FAQExtractorOutput)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/faq_extract.j2"
        self.model = model(config=model_config())

    def execute(self, state: GlobalState):
        questions = state.get("raw_questions", [])

        if len(questions) < int(os.getenv("QUESTIONS_TO_EXTRACT_FAQ", 5)):
            return Command(
                update={
                    "is_write_faq": False,
                }
            )

        # TODO: распарсить в Jinja
        format_questions = "\n".join(f"- {q}" for q in questions)

        template = self.prompt_manager.render(self.prompt_template, {})

        prompt = ChatPromptTemplate.from_messages([("system", template)])

        chain = prompt | self.model | self.parser

        output_result = chain.invoke(
            {
                "format_instructions": self.parser.get_format_instructions(),
                "all_questions": format_questions,
            }
        )["items"]

        # Обрабатываем данные экстрактора в формат с баллами
        arr_to_state = []
        for item in output_result:
            theme = Theme(text=item["theme"]["text"], score=item["theme"].get("score", 1.0))
            temp_questions = [
                Question(text=i["text"], score=i.get("score", 1.0), send_date=i["send_date"])
                for i in item["questions"]
            ]
            arr_to_state.append(FAQData(theme=theme, questions=temp_questions))

        return Command(
            update={
                "faq": arr_to_state,
                "raw_questions": [],
                "is_write_faq": True,
            }
        )

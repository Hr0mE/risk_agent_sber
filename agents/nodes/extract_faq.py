import os
from agents.nodes.base import BaseNode
from agents.prompts.base import PromptManager
from agents.state_management import (
    Command,
    NodeNames,
)
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import MessagesState
from models import MistralLargeModel as model
from langchain_core.output_parsers import JsonOutputParser
from agents.state_management import FAQExtractorOutput


class FAQExtractNode(BaseNode):
  def __init__(self, name = None):
    super().__init__(name=NodeNames.EXTRACT_FAQ.value)
    self.parser = JsonOutputParser(pydantic_object=FAQExtractorOutput)
    self.prompt_manager = PromptManager()
    self.prompt_template = "system/faq_extract.j2"

  def execute(self, state: MessagesState):
    questions = state.get("raw_questions", [])

    if len(questions) < os.getenv("QUESTIONS_TO_EXTRACT_FAQ", 5):
      return Command()
    
    # TODO: распарсить в Jinja
    format_questions = "\n".join(f"- {q}" for q in questions)

    template = self.prompt_manager.render(
      self.prompt_template,
      {
        "format_instructions": self.parser.get_format_instructions()
      }
    )

    prompt = ChatPromptTemplate.from_messages([("system", template)])

    chain = prompt | model | self.parser

    result = chain.invoke({
      "all_questions": format_questions,
    })

    return Command(
      update={
        "faq": result["items"],
        "raw_questions": [],
      }
    )
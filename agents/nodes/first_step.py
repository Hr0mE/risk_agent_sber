from langgraph.types import Command
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from agents.nodes.base import BaseNode
from agents.state_management import (
    GlobalState, 
    NodeNames
)


from agents.state_management.first_step_model import FirstStepDecisionModel as output_model

from agents.prompts.base import PromptManager
from agents.edges.conditions import ConditionHandler
from models import MistralLargeModel as model
from models.config import MistralLargeAPIConfig as model_config


class FirstStepNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.FIRST_STEP.value)
        self.parser = PydanticOutputParser(pydantic_object=output_model)
        
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/first_step.j2"
        
        self.model = model(config=model_config())
        
        self.options = [ # Ноды, в которые можно перейти из FirstStep 
            NodeNames.FINALIZE,
            NodeNames.SEARCH,
            NodeNames.RAG,
            NodeNames.WRITE
        ]
    
    def execute(self, state: GlobalState) -> Command:
        # Рендеринг промпта
        template = self.prompt_manager.render(
            self.prompt_template,
            {
                "options": self.options,
            }
        )
        
        prompt = ChatPromptTemplate.from_messages([("system", template)])
        chain = prompt | self.model | self.parser
        
        result = chain.invoke({
            "user_question": state.get("user_question", ""),
            "last_reason": state.get("last_reason", ""),
            "format_instructions": self.parser.get_format_instructions()
        })
        
        return Command(
            update={
                "final_decision": result.final_decision,
                "search_query": result.search_query,
                "rag_query": result.rag_query,
            },
            goto = ConditionHandler.evaluate_transition(
                source_node=self.name,
                result=result
            )
        )
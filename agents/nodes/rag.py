from langgraph.types import Command
from agents.nodes.base import BaseNode
from langchain_community.vectorstores.faiss import FAISS
from agents.state_management import (
    GlobalState, 
    NodeNames,
)
from models import NomicEmbedModel as embed
from models.config import NomicEmbedAPIConfig as model_config
from pathlib import Path


#TODO Настроить температуру

class RagNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.RAG.value)
        self.model = embed(config=model_config())
        self.path_to_db = Path(__file__).resolve().parents[2] / "database" / "faiss_db"

    def execute(self, state: GlobalState) -> dict:
        vectorstore = FAISS.load_local(self.path_to_db, self.model, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()

        #TODO Выдавать не один результат, а сразу много
        result = retriever.invoke(state.get("rag_query", ""))[0]

        return Command(
            update={"rag_results": result}
        )
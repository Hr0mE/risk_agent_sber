from agents.nodes.base import BaseNode
from langchain_community.vectorstores.faiss import FAISS
from agents.state_management import (
    ReasoningState, 
    NodeNames,
    Command
)
from models import MistralEmbedModel as embed

class RagNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.RAG.value)

    def execute(self, state: ReasoningState) -> dict:
        vectorstore = FAISS.load_local("./faiss_db", embed, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()

        result = retriever.invoke(state.rag_query)[0]

        return Command(
            update={"rag_results": result}
        )
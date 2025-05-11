from agents.nodes.base import BaseNode
from langchain_community.vectorstores.faiss import FAISS
from agents.state_management import (
    NodeNames,
    Command
)
from langgraph.graph import MessagesState
from models import MistralEmbedModel as embed

#TODO Настроить температуру

class RagNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.RAG.value)

    def execute(self, state: MessagesState) -> dict:
        vectorstore = FAISS.load_local("./faiss_db", embed, allow_dangerous_deserialization=True)
        retriever = vectorstore.as_retriever()

        #TODO Выдавать не один результат, а сразу много
        result = retriever.invoke(state.get("rag_query", ""))[0]

        return Command(
            update={"rag_results": result}
        )
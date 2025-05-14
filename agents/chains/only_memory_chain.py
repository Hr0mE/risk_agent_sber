from .base import BaseChain
from typing import List
from agents import nodes

class OnlyMemoryChain(BaseChain):
    """Полная цепочка выполнения с основными нодами"""
    
    def __init__(self):
        super().__init__()
        
        node_list: List[nodes.BaseNode] = [
            nodes.QuestionDecompositionNode,
            nodes.MannerExtractNode,
            nodes.WriteMannerToMemoryNode,
            nodes.GetMannerFromMemoryNode,

            nodes.StoreQuestionNode,
            nodes.FAQExtractNode,
            nodes.FAQWriteNode,
            nodes.GetFAQFromMemoryNode,

            nodes.ReasonNode,
        ]

        #TODO попробовать по-максимуму убрать goto и перенести всё сюда
        edge_list = [
            (nodes.QuestionDecompositionNode, nodes.MannerExtractNode),
            (nodes.MannerExtractNode, nodes.WriteMannerToMemoryNode),
            (nodes.WriteMannerToMemoryNode, nodes.GetMannerFromMemoryNode),

            (nodes.GetMannerFromMemoryNode, nodes.StoreQuestionNode),
            (nodes.StoreQuestionNode, nodes.FAQExtractNode),
            (nodes.FAQExtractNode, nodes.FAQWriteNode),
            (nodes.FAQWriteNode, nodes.GetFAQFromMemoryNode),

            (nodes.GetFAQFromMemoryNode, nodes.ReasonNode),
        ]

        # Регистрация нод
        for node in node_list:
            self.add_node(name=node().get_name(), node=node().execute)
        
        # Определение связей
        for (source_edge, target_edge) in edge_list:
            self.add_edge(source_edge().get_name(), target_edge().get_name())
     
        # Настройка точек входа/выхода
        self.set_entry_point(nodes.QuestionDecompositionNode().get_name())
        self.set_exit_point(nodes.ReasonNode().get_name())
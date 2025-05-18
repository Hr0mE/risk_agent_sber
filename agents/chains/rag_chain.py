from .base import BaseChain
from typing import List
from agents import nodes


class RagChain(BaseChain):
    """Цепочка выполнения без ноды веб-поиска"""

    def __init__(self):
        super().__init__()

        node_list: List[nodes.BaseNode] = [
            nodes.QuestionDecompositionNode,
            nodes.RagNode,
            nodes.CritiqueNode,
            nodes.FinalizeNode,
            nodes.FirstStepNode,
            nodes.ReasonNode,
            nodes.WriteNode,
        ]

        # TODO попробовать по-максимуму убрать goto и перенести всё сюда
        edge_list = [
            (nodes.QuestionDecompositionNode, nodes.ReasonNode),
            (nodes.ReasonNode, nodes.FirstStepNode),
            (nodes.WriteNode, nodes.CritiqueNode),
            (nodes.RagNode, nodes.WriteNode),
        ]

        # Регистрация нод
        for node in node_list:
            self.add_node(name=node().get_name(), node=node().execute)

        # Определение связей
        for source_edge, target_edge in edge_list:
            self.add_edge(source_edge().get_name(), target_edge().get_name())

        # Настройка точек входа/выхода
        self.set_entry_point(nodes.QuestionDecompositionNode().get_name())
        self.set_exit_point(nodes.FinalizeNode().get_name())

from .base import BaseChain
from agents import nodes

class FullExecutionChain(BaseChain):
    """Полная цепочка выполнения с основными нодами"""
    
    def __init__(self):
        super().__init__()
        
        node_list = [
            nodes.RagNode,
            nodes.FinalizeNode,
            nodes.CritiqueNode,
            nodes.FirstStepNode,
            nodes.ReasonNode,
            nodes.SearchNode,
            nodes.WriteNode
        ]

        #TODO попробовать по-максимуму убрать goto и перенести всё сюда
        edge_list = [
            (nodes.ReasonNode, nodes.FirstStepNode),
            (nodes.WriteNode, nodes.CritiqueNode),
            (nodes.SearchNode, nodes.WriteNode),
            (nodes.RagNode, nodes.WriteNode),
        ]

        # Регистрация нод
        for node in node_list:
            self.add_node(name=node.get_name(), node=node.execute)
        
        # Определение связей
        for (source_edge, target_edge) in edge_list:
            self.add_edge(source_edge.get_name(), target_edge.get_name())
     
        # Настройка точек входа/выхода
        self.set_entry_point(nodes.ReasonNode.get_name())
        self.set_exit_point(nodes.FinalizeNode.get_name())
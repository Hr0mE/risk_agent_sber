from agents import nodes

from .base import BaseChain


class FullExecutionChain(BaseChain):
  def __init__(self):
    super().__init__()

    node_list = [
      nodes.MannerExtractNode,
      nodes.WriteMannerToMemoryNode,
      nodes.GetMannerFromMemoryNode,
    ]

    edge_list = [
      (nodes.MannerExtractNode, nodes.WriteMannerToMemoryNode),
      (nodes.WriteMannerToMemoryNode, nodes.GetMannerFromMemoryNode)
    ]

    for node in node_list:
      self.add_node(name=node().get_name(), node=node().execute)

    for (source_edge, target_edge) in edge_list:
      self.add_edge(source_edge().get_name(), target_edge().get_name())
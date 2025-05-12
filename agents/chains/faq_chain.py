from agents import nodes

from .base import BaseChain


class FAQExecutionChain(BaseChain):
  def __init__(self):
    super().__init__()

    node_list = [
      nodes.StoreQuestionNode,
      nodes.FAQExtractNode,
      nodes.FAQWriteNode,
      nodes.GetFAQFromMemoryNode,
    ]

    edge_list = [
      (nodes.StoreQuestionNode, nodes.FAQExtractNode),
      (nodes.FAQExtractNode, nodes.FAQWriteNode),
      (nodes.FAQWriteNode, nodes.GetFAQFromMemoryNode),
    ]

    for node in node_list:
      self.add_node(name=node().get_name(), node=node().execute)

    for (source_edge, target_edge) in edge_list:
      self.add_edge(source_edge().get_name(), target_edge().get_name())
from typing import Dict, List, Tuple, Callable
from langgraph.graph import StateGraph
from langgraph.graph import MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Checkpointer

# TODO сделать условные переходы

class BaseChain:
    """Базовый класс для всех цепочек выполнения"""
    
    def __init__(self):
        # Словарь зарегистрированных нод: {имя_ноды: функция}
        self.nodes: Dict[str, Callable] = {}

        # Список связей между нодами: [(from_node, to_node)]
        self.edges: List[Tuple[str, str]] = []

        self.entry_point: str = None
        self.exit_point: str = None

    def build(self, state: MessagesState, name: str = None, checkpointer: Checkpointer = None) -> CompiledStateGraph:
        """Собирает граф из зарегистрированных компонентов"""
        self._validate_chain()
        
        workflow = StateGraph(state)
        
        # Добавляем все ноды
        for name, node in self.nodes.items():
            workflow.add_node(name, node)
        
        # Добавляем связи
        for source, target in self.edges:
            workflow.add_edge(source, target)
        
        # Настраиваемreason точки входа/выхода
        if self.entry_point:
            workflow.set_entry_point(self.entry_point)
        if self.exit_point:
            workflow.set_finish_point(self.exit_point)
            
        return workflow.compile(name=name, checkpointer=checkpointer)

    def _validate_chain(self) -> None:
        """Проверяет целостность цепочки"""
        if not self.nodes:
            raise ValueError("Chain must contain at least one node")
            
        if not self.edges:
            raise ValueError("Chain must contain at least one edge")
            
        if not self.entry_point:
            raise ValueError("Entry point must be defined")
        
        if not self.exit_point:
            raise ValueError("Exit point must be defined")
            

        # Проверяем существование нод в связях
        all_nodes = set(self.nodes.keys())
        for source, target in self.edges:
            if source not in all_nodes:
                raise ValueError(f"Source node '{source}' not registered")
            if target not in all_nodes:
                raise ValueError(f"Target node '{target}' not registered")

    def add_node(self, name: str, node: Callable) -> None:
        """Регистрирует ноду в цепочке"""
        if name in self.nodes:
            raise KeyError(f"Node '{name}' already exists")
        self.nodes[name] = node

    def add_edge(self, source: str, target: str) -> None:
        """Добавляет связь между нодами"""
        self.edges.append((source, target))

    #TODO возможно, переписать на получение ноды и извлекать имя в самой функции
    def set_entry_point(self, node_name: str) -> None:
        """Устанавливает стартовую ноду"""
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not registered")
        self.entry_point = node_name

    def set_exit_point(self, node_name: str) -> None:
        """Устанавливает финишную ноду"""
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not registered")
        self.exit_point = node_name
from agents.state_management import NodeNames
from agents.state_management.first_step_model import FirstStepDecisionModel
from agents.state_management import Command

class ConditionHandler:
    @staticmethod
    def handle_first_step(decision: FirstStepDecisionModel) -> NodeNames:
        """
        Определяем следующую ноду на основе решения из FirstStepDecision
        Логика проверок:
        1. Если решение требует поиска, но запрос пустой - завершаем
        2. Если решение требует RAG, но запрос пустой - завершаем
        3. В остальных случаях следуем решению
        """
        next_node = decision.final_decision
        
        # Проверяем необходимые условия для переходов
        if next_node == NodeNames.SEARCH and not decision.search_query:
            return NodeNames.FINALIZE
            
        if next_node == NodeNames.RAG and not decision.rag_query:
            return NodeNames.FINALIZE
            
        return next_node
    

    @classmethod
    def evaluate_transition(cls, source_node: NodeNames, result: object) -> NodeNames:
        """
        Главный роутер для обработки переходов между нодами
        """
        if source_node == NodeNames.FIRST_STEP:
            if not isinstance(result, FirstStepDecisionModel):
                raise TypeError("FirstStep transition requires agents.state_management.first_step_model.FirstStepDecision output")
            return cls.handle_first_step(result)
       
        raise NotImplementedError(f"Transition from {source_node} not implemented")
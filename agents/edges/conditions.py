from agents.state_management import NodeNames
from agents.state_management import (
    FirstStepDecisionModel,
    CritiqueDecisionModel
)

class ConditionHandler:
    @staticmethod
    def handle_first_step(decision: FirstStepDecisionModel) -> NodeNames:
        """
        Определяем следующую ноду на основе решения из FirstStepDecisionModel
        Логика проверок:
        1. Если решение требует поиска, но запрос пустой - завершаем
        2. Если решение требует RAG, но запрос пустой - завершаем
        3. В остальных случаях следуем решению
        """
        next_node: str = decision.final_decision

        # Проверяем необходимые условия для переходов
        if next_node == NodeNames.SEARCH and not decision.search_query:
            return NodeNames.FINALIZE.value
            
        if next_node == NodeNames.RAG and not decision.rag_query:
            return NodeNames.FINALIZE.value
            
        return next_node
    
    @staticmethod
    def handle_critique(decision: CritiqueDecisionModel) -> NodeNames:
        """
        Определяем следующую ноду на основе решения из CritiqueDecisionModel
        Логика проверок:
        1. Если решение требует поиска, но запрос пустой - завершаем
        2. Если решение требует RAG, но запрос пустой - завершаем
        3. В остальных случаях переходим в FINALIZE
        """
        next_node: str = decision.final_decision

        # Проверяем необходимые условия для переходов
        if next_node == NodeNames.SEARCH and not decision.search_query:
            return NodeNames.FINALIZE.value
            
        if next_node == NodeNames.RAG and not decision.rag_query:
            return NodeNames.FINALIZE.value
            
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
        
        elif source_node == NodeNames.CRITIQUE:
            if not isinstance(result, CritiqueDecisionModel):
                raise TypeError("Critique transition requires agents.state_management.critique_model.CritiqueDecisionModel output")
            
            return cls.handle_critique(result)
    
        raise NotImplementedError(f"Transition from {source_node} not implemented")
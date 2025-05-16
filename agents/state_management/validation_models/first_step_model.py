from pydantic import BaseModel, Field


class FirstStepDecisionModel(BaseModel):
    """Модель для первого шага обработки запроса"""
    search_query: str = Field(description="Текст поискового запроса для веб-поиска")
    rag_query: str = Field(description="Текст запроса для поиска по внутренней базе документов")
    final_decision: str = Field(description=f"Итоговое решение о следующем шаге")


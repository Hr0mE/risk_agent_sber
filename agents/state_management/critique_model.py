from pydantic import BaseModel, Field

class CritiqueDecisionModel(BaseModel):
    """Критика выступления"""

    thoughts: str = Field(description="Мысли по поводу ответа")
    critique: str = Field(description="Конструктивная критика ответа - что нужно поправить или доработать")
    search_query: str = Field(description="Текст поискового запроса на поиск данных в интернете, если нужен")
    rag_query: str = Field(description="Текст поисковогого запроса на поиск по внутренней базе документов, если нужен")
    final_decision: str = Field(description="Итоговое решение, должно быть одно из следующих: good (если нет новой критики, есть отрывки из книг и речь можно считать написаной), search (требуется поиск данных в интернете), fix (если требуется переписать или доработать ответ)")


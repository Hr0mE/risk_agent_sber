from models import NomicEmbedModel
from models.config import NomicEmbedAPIConfig as model_config
import numpy as np
from typing import List, Optional

model = NomicEmbedModel(config=model_config())


def find_similar_theme(theme: str, themes: List[str], threshold=0.78) -> Optional[str]:
    """Поиск схожей темы по смыслу среди существующих тем

    Args:
        theme (str): тема, которой надо найти схожую
        themes (List[str]): все существующие темы
        threshold (float, optional): порог сходства(от 0 до 1). Defaults to 0.78.

    Returns:
        Optional[str]: найденная тема или None, если такой нет
    """
    for existing_theme in themes:
        emb1, emb2 = model.embed_query(theme), model.embed_query(existing_theme)
        
        if np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)) >= threshold:
            return existing_theme

    return None

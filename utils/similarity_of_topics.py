import difflib

from typing import List, Union


def find_similar_theme(theme: str, themes: List[str], threshold=0.9) -> Union[str, None]:
    """Вычисление схожести тем"""
    for existing_theme in themes:
        similarity = difflib.SequenceMatcher(None, theme.lower(), existing_theme.lower()).ratio()
        if similarity >= threshold:
            return existing_theme

    return None

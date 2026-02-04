from typing import Literal

ClauseType = Literal[
    "Obligation",
    "Right",
    "Prohibition",
    "Neutral"
]


def tag_clause_type(clause_text: str) -> ClauseType:
    """
    Classifies a clause into:
    - Obligation
    - Right
    - Prohibition
    - Neutral
    """

    if not clause_text:
        return "Neutral"

    text = clause_text.lower()

    if "shall not" in text or "must not" in text:
        return "Prohibition"

    if "shall" in text or "must" in text:
        return "Obligation"

    if "may" in text:
        return "Right"

    return "Neutral"

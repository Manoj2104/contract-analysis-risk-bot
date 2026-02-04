def detect_obligation_type(text):
    text = text.lower()

    if any(k in text for k in ["shall", "must", "is required to"]):
        return "Obligation"
    if any(k in text for k in ["may", "is entitled to"]):
        return "Right"
    if any(k in text for k in ["shall not", "must not", "is prohibited"]):
        return "Prohibition"

    return "Neutral"

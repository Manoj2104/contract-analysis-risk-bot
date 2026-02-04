def is_unilateral(text):
    text = text.lower()
    if "company may terminate" in text and "employee may terminate" not in text:
        return True
    if "sole discretion" in text:
        return True
    return False

def detect_penalty(text):
    keywords = ["penalty", "liquidated damages", "fine"]
    return any(k in text.lower() for k in keywords)

def detect_indemnity(text):
    return "indemnify" in text.lower()

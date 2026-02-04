import re

def detect_language(text: str) -> str:
    """
    Detects if text is Hindi or English.
    Returns: 'hi' or 'en'
    """

    if not text:
        return "en"

    # Hindi Unicode block
    hindi_chars = re.findall(r"[\u0900-\u097F]", text)

    # If more than a few Hindi chars → Hindi document
    if len(hindi_chars) > 10:
        return "hi"

    return "en"

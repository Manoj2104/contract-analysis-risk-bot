import re

# 🔑 Hindi → English legal keyword mapping
HINDI_TO_ENGLISH_MAP = {
    "किराया": "rent",
    "भुगतान": "payment",
    "राशि": "amount",
    "सुरक्षा जमा": "security deposit",
    "जमा": "deposit",
    "समाप्त": "termination",
    "समाप्ति": "termination",
    "नोटिस": "notice",
    "अवधि": "duration",
    "समयावधि": "term",
    "न्यायालय": "court",
    "क्षेत्राधिकार": "jurisdiction",
    "कानून": "law",
    "उत्तरदायित्व": "liability",
    "क्षतिपूर्ति": "indemnity",
    "गोपनीय": "confidential",
    "समझौता": "agreement",
    "पक्ष": "party",
    "मकान मालिक": "lessor",
    "किरायेदार": "lessee"
}


def normalize_hindi_to_english(text: str) -> str:
    """
    Converts Hindi legal keywords into English
    for NLP compatibility.
    """

    normalized = text.lower()

    for hi, en in HINDI_TO_ENGLISH_MAP.items():
        normalized = re.sub(hi, en, normalized)

    return normalized

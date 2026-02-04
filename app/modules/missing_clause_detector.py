from typing import List, Dict
import re

# ==========================================================
# UNIVERSAL MANDATORY CLAUSES (INDIA + HINDI AWARE)
# ==========================================================

MANDATORY_CLAUSES_BY_TYPE: Dict[str, Dict[str, List[str]]] = {

    # ------------------------------------------------------
    # LEASE / RENT AGREEMENT (INDIA)
    # ------------------------------------------------------
    "Lease Agreement": {

        "Termination": [
            # English
            "terminate", "termination", "evict", "eviction",
            "notice", "notice period",
            "vacant possession", "fails to pay", "default",

            # Hindi
            "समाप्त", "समाप्ति", "नोटिस",
            "खाली", "बेदखल",
            "किराया न देने"
        ],

        "Payment Terms": [
            # English
            "rent", "rs", "rupees", "payable",
            "advance", "deposit", "security deposit",
            "electricity charges", "water charges",

            # Hindi
            "किराया", "भुगतान", "राशि",
            "जमा", "अग्रिम",
            "बिजली", "पानी"
        ],

        # Indian-style jurisdiction (explicit + implicit)
        "Jurisdiction": [
            # English
            "jurisdiction", "courts at", "courts of",
            "subject to", "laws of india",
            "executed at", "place of execution",
            "agreement is made at",
            "agreement of rent is made at",

            # Hindi
            "क्षेत्राधिकार", "न्यायालय",
            "भारत के कानून",
            "अधीन होगा", "निष्पादित"
        ],

        # Implicit liability / deduction detection
        "Limitation of Liability": [
            # English
            "not liable", "shall not be liable",
            "deduct from advance", "deduct from deposit",
            "deduct such amount",
            "damages", "arrears",
            "liability", "indemnify",

            # Hindi
            "उत्तरदायित्व", "जिम्मेदारी",
            "कटौती", "हानि",
            "क्षतिपूर्ति", "देय नहीं"
        ],
    },

    # ------------------------------------------------------
    # EMPLOYMENT AGREEMENT
    # ------------------------------------------------------
    "Employment Agreement": {

        "Termination": [
            "terminate", "termination",
            "resignation", "dismissal",
            "notice", "notice period",

            # Hindi
            "इस्तीफा", "समाप्ति", "नोटिस"
        ],

        "Payment Terms": [
            "salary", "wages", "ctc",
            "remuneration", "deduction",
            "payable",

            # Hindi
            "वेतन", "तनख्वाह", "भुगतान"
        ],

        "Confidentiality": [
            "confidential", "nda",
            "non disclosure",
            "trade secret",
            "proprietary information",

            # Hindi
            "गोपनीय", "गोपनीय जानकारी"
        ],

        "Jurisdiction": [
            "jurisdiction", "courts of",
            "governing law", "laws of india",

            # Hindi
            "क्षेत्राधिकार", "न्यायालय"
        ],

        "Limitation of Liability": [
            "limitation of liability",
            "not liable",
            "maximum liability",

            # Hindi
            "उत्तरदायित्व", "जिम्मेदारी"
        ],
    },

    # ------------------------------------------------------
    # SERVICE / CONSULTING AGREEMENT
    # ------------------------------------------------------
    "Service Agreement": {

        "Scope of Work": [
            "scope of work",
            "services",
            "deliverables",

            # Hindi
            "कार्य क्षेत्र", "सेवाएं"
        ],

        "Payment Terms": [
            "fees", "invoice",
            "payment terms",
            "consideration",

            # Hindi
            "फीस", "भुगतान"
        ],

        "Termination": [
            "terminate", "termination",
            "notice period",

            # Hindi
            "समाप्ति", "नोटिस"
        ],

        "Confidentiality": [
            "confidential",
            "nda", "non disclosure",

            # Hindi
            "गोपनीय"
        ],

        "Limitation of Liability": [
            "limitation of liability",
            "not liable",

            # Hindi
            "उत्तरदायित्व"
        ],

        "Jurisdiction": [
            "jurisdiction",
            "courts of",
            "governing law",

            # Hindi
            "क्षेत्राधिकार", "न्यायालय"
        ],
    },

    # ------------------------------------------------------
    # NDA
    # ------------------------------------------------------
    "NDA": {

        "Confidentiality": [
            "confidential",
            "confidential information",
            "non disclosure",
            "nda",

            # Hindi
            "गोपनीय", "गोपनीय जानकारी"
        ],

        "Exclusions": [
            "public domain",
            "already known",
            "lawfully obtained",

            # Hindi
            "सार्वजनिक", "पहले से ज्ञात"
        ],

        "Duration": [
            "term", "duration", "period",

            # Hindi
            "अवधि", "समय"
        ],

        "Jurisdiction": [
            "jurisdiction",
            "governing law",

            # Hindi
            "क्षेत्राधिकार"
        ],
    },

    # ------------------------------------------------------
    # GENERIC / UNKNOWN CONTRACT (Fallback)
    # ------------------------------------------------------
    "Generic": {

        "Termination": [
            "terminate", "termination", "notice",
            "समाप्त", "समाप्ति", "नोटिस"
        ],

        "Payment Terms": [
            "payment", "amount", "fees",
            "भुगतान", "राशि"
        ],

        "Jurisdiction": [
            "jurisdiction", "courts at",
            "courts of", "governing law",
            "laws of india",

            # Indian implicit patterns
            "executed at", "place of execution",
            "agreement is made at",

            # Hindi
            "क्षेत्राधिकार", "न्यायालय",
            "भारत के कानून"
        ],

        "Limitation of Liability": [
            "limitation of liability",
            "not liable",

            # Hindi
            "उत्तरदायित्व", "जिम्मेदारी"
        ],
    }
}


# ==========================================================
# MAIN DETECTOR (OCR + HINDI SAFE)
# ==========================================================

def detect_missing_clauses(
    contract_text: str,
    contract_type: str = "Generic"
) -> List[str]:
    """
    FINAL – India + Hindi aware missing clause detector

    ✔ English contracts
    ✔ Hindi contracts
    ✔ Mixed contracts
    ✔ OCR tolerant
    """

    # Empty / unreadable file
    if not contract_text or not contract_text.strip():
        return list(
            MANDATORY_CLAUSES_BY_TYPE.get(
                contract_type,
                MANDATORY_CLAUSES_BY_TYPE["Generic"]
            ).keys()
        )

    # Normalize OCR / PDF noise
    # IMPORTANT: keep Hindi Unicode range
    text = contract_text.lower()
    text = re.sub(r"[^\w\s\u0900-\u097F]", " ", text)
    text = re.sub(r"\s+", " ", text)

    rules = MANDATORY_CLAUSES_BY_TYPE.get(
        contract_type,
        MANDATORY_CLAUSES_BY_TYPE["Generic"]
    )

    missing: List[str] = []

    for clause_name, keywords in rules.items():
        if not any(keyword in text for keyword in keywords):
            missing.append(clause_name)

    return missing

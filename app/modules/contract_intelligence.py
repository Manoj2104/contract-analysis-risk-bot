import re
from modules.language_detector import detect_language
from modules.hindi_normalizer import normalize_hindi_to_english



def extract_contract_intelligence(text: str) -> dict:
    text_l = text.lower()

    data = {
        "parties": [],
        "financial_amounts": [],
        "obligations": [],
        "deliverables": [],
        "timeline": [],
        "termination": [],
        "jurisdiction": None,
        "rights_ip": [],
        "confidentiality": False,
        "languages_detected": []
    }

    # ---------------------------
    # 1. Parties
    # ---------------------------
    party_patterns = [
        r"between\s+(.*?)\s+and\s+(.*?)[\.,]",
        r"lessor|lessee|tenant|owner|employer|employee"
    ]
    for p in party_patterns:
        if re.search(p, text_l):
            data["parties"].append("Parties identified in agreement")
            break

    # ---------------------------
    # 2. Financial Amounts
    # ---------------------------
    amounts = re.findall(r"rs\.?\s?\d+[,\d]*|\₹\s?\d+[,\d]*|\d+\s?rupees", text_l)
    data["financial_amounts"] = list(set(amounts))

    # ---------------------------
    # 3. Obligations & Liabilities
    # ---------------------------
    if re.search(r"shall|must|required to|liable|responsible for", text_l):
        data["obligations"].append("Binding obligations detected")

    # ---------------------------
    # 4. Deliverables / Performance
    # ---------------------------
    if re.search(r"deliver|provide|perform|service level|sla|completion", text_l):
        data["deliverables"].append("Deliverables or performance commitments detected")

    # ---------------------------
    # 5. Timeline / Duration
    # ---------------------------
    timelines = re.findall(
        r"\d+\s?(days|months|years)|from\s+\d{1,2}/\d{1,2}/\d{2,4}",
        text_l
    )
    data["timeline"] = timelines

    # ---------------------------
    # 6. Termination Conditions
    # ---------------------------
    if re.search(r"terminate|termination|evict|cancel|breach", text_l):
        data["termination"].append("Termination conditions present")

    # ---------------------------
    # 7. Jurisdiction & Governing Law
    # ---------------------------
    match = re.search(r"jurisdiction|governing law|courts of ([a-z\s]+)", text_l)
    if match:
        data["jurisdiction"] = match.group(0)

    # ---------------------------
    # 8. Rights & Ownership (IP)
    # ---------------------------
    if re.search(r"intellectual property|ip rights|ownership|copyright|patent", text_l):
        data["rights_ip"].append("IP or ownership clause detected")

    # ---------------------------
    # 9. Confidentiality / NDA
    # ---------------------------
    if re.search(r"confidential|non-disclosure|nda|privacy", text_l):
        data["confidentiality"] = True

    # ---------------------------
    # 10. Multilingual Handling
    # ---------------------------
    if re.search(r"[அ-ஹ]", text):
        data["languages_detected"].append("Tamil")
    if re.search(r"[अ-ह]", text):
        data["languages_detected"].append("Hindi")
    if re.search(r"[a-zA-Z]", text):
        data["languages_detected"].append("English")

    return data

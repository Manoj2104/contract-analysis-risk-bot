# modules/contract_entity_normalizer.py
import re

CONTRACT_SCHEMA = {
    "Parties": [],
    "Financial Amounts": [],
    "Obligations & Liabilities": [],
    "Deliverables & Performance": [],
    "Timeline / Duration": [],
    "Termination Conditions": [],
    "Jurisdiction & Governing Law": [],
    "Rights & Ownership": [],
    "Confidentiality & NDA": []
}

# -------------------------------------------------
# CONTRACT TYPE ROLE MAP
# -------------------------------------------------
ROLE_MAP = {
    "Lease Agreement": ("HOUSE OWNER", "TENANT"),
    "Employment Agreement": ("EMPLOYER", "EMPLOYEE"),
    "Service Agreement": ("CLIENT", "SERVICE PROVIDER"),
    "Vendor Contract": ("PURCHASER", "VENDOR"),
    "Partnership Deed": ("PARTNER A", "PARTNER B"),
    "NDA": ("DISCLOSING PARTY", "RECEIVING PARTY")
}

# -------------------------------------------------
# PERSON NAME EXTRACTION (ORDER SAFE)
# -------------------------------------------------
def extract_all_person_names(text: str):
    matches = re.finditer(
        r"(Mr\.?|Mrs\.?|Ms\.?)\s+[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z.]+)+",
        text
    )
    names = []
    for m in matches:
        name = m.group().strip()
        if len(name.split()) >= 2:
            names.append(name)
    return list(dict.fromkeys(names))


# -------------------------------------------------
# ROLE-BASED EXTRACTION
# -------------------------------------------------
def extract_party_by_keywords(text: str, keywords):
    for kw in keywords:
        pattern = rf"{kw}.*?(Mr\.?\s+[A-Z][A-Za-z.\s]+?)(?:,| aged| son of| daughter of)"
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if m:
            name = m.group(1).strip()
            if len(name.split()) >= 2:
                return name
    return None


# -------------------------------------------------
# FINANCIAL EXTRACTION
# -------------------------------------------------
def extract_money(text: str, keywords):
    for kw in keywords:
        pattern = rf"{kw}.*?(₹|rs\.?)\s*([\d,]{{3,}})"
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(2)
    return None


def extract_duration_months(text: str):
    m = re.search(r"(\d{2}|11)\s*months", text, re.IGNORECASE)
    return m.group(1) if m else None


def extract_notice_days(text: str):
    m = re.search(r"(\d{2,3})\s*days", text, re.IGNORECASE)
    return m.group(1) if m else None


def extract_jurisdiction(text: str):
    triggers = ["jurisdiction", "courts at", "subject to"]
    if not any(t in text.lower() for t in triggers):
        return []

    places = []
    for p in ["chennai", "tamil nadu", "india", "bangalore", "karnataka"]:
        if p in text.lower():
            places.append(p.upper())
    return list(set(places))


# -------------------------------------------------
# MAIN NORMALIZER (ALL CONTRACT TYPES)
# -------------------------------------------------
def normalize_contract_entities(
    raw_entities: dict,
    text: str,
    contract_type: str = "Lease Agreement"
):
    result = {k: [] for k in CONTRACT_SCHEMA}
    text_lower = text.lower()

    role_a, role_b = ROLE_MAP.get(contract_type, ("PARTY A", "PARTY B"))

    # -------------------------------
    # PARTIES
    # -------------------------------
    party_a = extract_party_by_keywords(
        text,
        [role_a.lower(), "owner", "employer", "client", "vendor", "partner"]
    )

    party_b = extract_party_by_keywords(
        text,
        [role_b.lower(), "tenant", "employee", "service provider", "purchaser", "partner"]
    )

    # FINAL FALLBACK → first two names
    if not party_a or not party_b:
        names = extract_all_person_names(text)
        if len(names) >= 2:
            party_a = party_a or names[0]
            party_b = party_b or names[1]

    result["Parties"].append(
        f"{role_a}: {party_a if party_a else 'The first party'} is a party to this agreement."
    )
    result["Parties"].append(
        f"{role_b}: {party_b if party_b else 'The second party'} is a party to this agreement."
    )

    # -------------------------------
    # FINANCIAL AMOUNTS (TYPE AWARE)
    # -------------------------------
    if contract_type == "Lease Agreement":
        rent = extract_money(text, ["rent"])
        if rent:
            result["Financial Amounts"].append(
                f"Monthly Rent: The tenant must pay ₹{rent} per month."
            )

    elif contract_type == "Employment Agreement":
        salary = extract_money(text, ["salary", "remuneration"])
        if salary:
            result["Financial Amounts"].append(
                f"Salary: The employee will be paid ₹{salary} as per the agreement."
            )

    elif contract_type == "Service Agreement":
        fees = extract_money(text, ["fees", "service charges"])
        if fees:
            result["Financial Amounts"].append(
                f"Service Fees: The client shall pay ₹{fees} for services rendered."
            )

    elif contract_type == "Vendor Contract":
        price = extract_money(text, ["price", "invoice", "amount"])
        if price:
            result["Financial Amounts"].append(
                f"Contract Value: The purchaser shall pay ₹{price} for supplied goods."
            )

    # -------------------------------
    # OBLIGATIONS
    # -------------------------------
    result["Obligations & Liabilities"].append(
        "The parties must perform their respective duties and obligations as stated in the agreement."
    )

    # -------------------------------
    # TIMELINE
    # -------------------------------
    months = extract_duration_months(text)
    if months:
        result["Timeline / Duration"].append(
            f"Agreement Duration: The agreement is valid for {months} months."
        )

    notice = extract_notice_days(text)
    if notice:
        result["Timeline / Duration"].append(
            f"Notice Period: {notice} days’ advance notice is required for termination."
        )

    # -------------------------------
    # TERMINATION
    # -------------------------------
    if "terminate" in text_lower:
        result["Termination Conditions"].append(
            "The agreement may be terminated subject to conditions mentioned in the contract."
        )

    # -------------------------------
    # JURISDICTION
    # -------------------------------
    result["Jurisdiction & Governing Law"] = extract_jurisdiction(text)

    # -------------------------------
    # RIGHTS & OWNERSHIP
    # -------------------------------
    result["Rights & Ownership"].append(
        "Each party retains rights and ownership as specified under the agreement."
    )

    # -------------------------------
    # CONFIDENTIALITY (STRICT)
    # -------------------------------
    if any(
        phrase in text_lower
        for phrase in [
            "confidential information",
            "non-disclosure agreement",
            "non disclosure",
            "nda"
        ]
    ):
        result["Confidentiality & NDA"].append(
            "Confidentiality obligations are expressly mentioned in this agreement."
        )
    else:
        result["Confidentiality & NDA"].append(
            "No confidentiality or non-disclosure obligations are mentioned in this agreement."
        )

    return result

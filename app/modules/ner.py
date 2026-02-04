import spacy
import re
from typing import Dict, List

# -------------------------------------------------
# Load spaCy model ONCE (IMPORTANT for performance)
# -------------------------------------------------
nlp = spacy.load("en_core_web_sm")


def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extracts and cleans key entities from contract text.

    Returns:
    {
        "ORG": [...],
        "DATE": [...],
        "MONEY": [...]
    }

    Designed for:
    - UI display
    - Risk analysis context
    - Hackathon demos (clean output)
    """

    if not text:
        return {"ORG": [], "DATE": [], "MONEY": []}

    doc = nlp(text)

    orgs = set()
    dates = set()
    money = set()

    # -----------------------------
    # spaCy-based entity extraction
    # -----------------------------
    for ent in doc.ents:
        ent_text = ent.text.strip()

        # ---- ORGANIZATIONS ----
        if ent.label_ == "ORG":
            # Filter junk / placeholders
            if (
                ent_text.lower() not in ["company", "employee", "employer"]
                and not any(char.isdigit() for char in ent_text)
                and "inr" not in ent_text.lower()
                and "₹" not in ent_text
                and len(ent_text) > 2
            ):
                orgs.add(ent_text)

        # ---- DATES ----
        elif ent.label_ == "DATE":
            # Ignore vague durations like "24 months"
            if not any(
                word in ent_text.lower()
                for word in ["month", "months", "year", "years"]
            ):
                dates.add(ent_text)

    # -----------------------------
    # Custom MONEY extraction
    # (More reliable than spaCy)
    # -----------------------------
    money_matches = re.findall(
        r"(₹\s?\d+(?:,\d{3})*(?:\.\d+)?|INR\s?\d+(?:,\d{3})*(?:\.\d+)?)",
        text,
        flags=re.I
    )

    for m in money_matches:
        money.add(m.strip())

    return {
        "ORG": sorted(orgs),
        "DATE": sorted(dates),
        "MONEY": sorted(money)
    }


# -------------------------------------------------
# BACKWARD COMPATIBILITY
# -------------------------------------------------
# Older code/tests may still call get_entities()
# This prevents breaking changes.

def get_entities(text: str) -> Dict[str, List[str]]:
    return extract_entities(text)

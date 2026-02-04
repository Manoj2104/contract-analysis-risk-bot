from typing import List, Dict

# =================================================
# AMBIGUOUS LEGAL TERMS (CATEGORIZED)
# =================================================

AMBIGUOUS_TERMS: Dict[str, Dict] = {
    "reasonable": {
        "category": "Subjective",
        "severity": 2,
        "suggestion": "Define objective standards or measurable criteria."
    },
    "reasonably": {
        "category": "Subjective",
        "severity": 2,
        "suggestion": "Specify exact conditions instead of subjective judgment."
    },
    "best efforts": {
        "category": "Obligation",
        "severity": 3,
        "suggestion": "Replace with clearly defined obligations or milestones."
    },
    "commercially reasonable": {
        "category": "Subjective",
        "severity": 3,
        "suggestion": "Define industry benchmarks or financial limits."
    },
    "from time to time": {
        "category": "Timeline",
        "severity": 2,
        "suggestion": "Specify frequency or fixed intervals."
    },
    "as soon as possible": {
        "category": "Timeline",
        "severity": 3,
        "suggestion": "Replace with a defined number of days."
    },
    "material": {
        "category": "Scope",
        "severity": 2,
        "suggestion": "Define what constitutes a material breach or change."
    },
    "significant": {
        "category": "Scope",
        "severity": 2,
        "suggestion": "Quantify what is considered significant."
    },
    "substantial": {
        "category": "Scope",
        "severity": 2,
        "suggestion": "Replace with numerical or objective thresholds."
    },
    "at its discretion": {
        "category": "Discretion",
        "severity": 3,
        "suggestion": "Limit discretion with conditions or mutual consent."
    }
}

# =================================================
# BASIC DETECTOR (BACKWARD COMPATIBLE)
# =================================================

def detect_ambiguity(clause_text: str) -> List[str]:
    """
    Basic ambiguity detector (legacy-compatible).

    Returns:
    - List of ambiguous terms found
    """

    if not clause_text:
        return []

    text = clause_text.lower()
    return [term for term in AMBIGUOUS_TERMS if term in text]


# =================================================
# ADVANCED AMBIGUITY ANALYSIS
# =================================================

def analyze_ambiguity(clause_text: str) -> Dict:
    """
    Performs advanced ambiguity analysis.

    Returns:
    {
        found_terms,
        severity_score,
        risk_level,
        categories,
        suggestions,
        explanation
    }
    """

    if not clause_text:
        return {
            "found_terms": [],
            "severity_score": 0,
            "risk_level": "Low",
            "categories": [],
            "suggestions": [],
            "explanation": "No clause text provided."
        }

    text = clause_text.lower()

    found = []
    severity_score = 0
    categories = set()
    suggestions = []

    for term, meta in AMBIGUOUS_TERMS.items():
        if term in text:
            found.append(term)
            severity_score += meta["severity"]
            categories.add(meta["category"])
            suggestions.append(meta["suggestion"])

    # Risk level mapping
    if severity_score >= 6:
        risk_level = "High"
    elif severity_score >= 3:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    explanation = (
        "Clause contains vague language that may lead to multiple interpretations "
        "and potential disputes."
        if found else
        "No ambiguous legal language detected."
    )

    return {
        "found_terms": found,
        "severity_score": severity_score,
        "risk_level": risk_level,
        "categories": list(categories),
        "suggestions": list(set(suggestions)),
        "explanation": explanation
    }


# =================================================
# UI-FRIENDLY SUMMARY (OPTIONAL)
# =================================================

def format_ambiguity_summary(analysis: Dict) -> str:
    """
    Converts ambiguity analysis into a user-friendly summary.
    """

    if not analysis["found_terms"]:
        return "✅ No ambiguous language detected."

    return (
        f"⚠️ Ambiguous terms detected: {', '.join(analysis['found_terms'])}\n"
        f"Risk Level: {analysis['risk_level']}\n"
        f"Categories: {', '.join(analysis['categories'])}"
    )

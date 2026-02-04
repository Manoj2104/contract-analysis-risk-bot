from typing import Dict, List


# Clause Classification (Improved & Ordered)

def classify_clause(clause: str) -> str:

    text = clause.lower()

    if any(k in text for k in ["terminate", "termination", "termination of this agreement"]):
        return "Termination"

    if any(k in text for k in ["non-compete", "non compete", "competing", "restraint of trade"]):
        return "Non-Compete"

    if any(k in text for k in ["confidential", "non-disclosure", "confidential information"]):
        return "Confidentiality"

    if any(k in text for k in ["salary", "compensation", "remuneration", "fees", "payment"]):
        return "Compensation"

    return "General"


# Risk Assessment Engine (Advanced & Explainable)

def assess_risk(clause: str) -> Dict:
    """
    Performs structured risk analysis for a single clause.

    Returns:
    {
        type,
        risk_level,
        score,
        reasons,
        suggestions
    }
    """

    text = clause.lower()
    score = 0
    reasons: List[str] = []
    suggestions: List[str] = []

    clause_type = classify_clause(clause)

    # -----------------------------
    # Risk phrase libraries
    # -----------------------------

    termination_red_flags = [
        "without notice",
        "without prior notice",
        "at any time",
        "immediate termination",
        "sole discretion"
    ]

    vague_terms = [
        "reasonable",
        "as soon as possible",
        "best efforts"
    ]

    # -----------------------------
    # TERMINATION
    # -----------------------------

    if clause_type == "Termination":
        if any(p in text for p in termination_red_flags):
            score += 45
            reasons.append(
                "Allows termination without adequate notice or safeguards."
            )
            suggestions.append(
                "Add a minimum notice period (e.g., 30 days) and termination for cause."
            )
        else:
            score += 20
            reasons.append(
                "Termination clause exists with defined conditions."
            )

    # -----------------------------
    # NON-COMPETE
    # -----------------------------

    elif clause_type == "Non-Compete":
        score += 35
        reasons.append(
            "Restricts future employment or business opportunities."
        )
        suggestions.append(
            "Limit non-compete by duration, geography, and scope of work."
        )

    # -----------------------------
    # CONFIDENTIALITY
    # -----------------------------

    elif clause_type == "Confidentiality":
        score += 10
        reasons.append(
            "Imposes confidentiality obligations."
        )

        if "in perpetuity" in text or "forever" in text:
            score += 10
            reasons.append(
                "Confidentiality obligation has no time limit."
            )
            suggestions.append(
                "Limit confidentiality duration (e.g., 2–5 years)."
            )

    # -----------------------------
    # COMPENSATION
    # -----------------------------

    elif clause_type == "Compensation":
        if not any(k in text for k in ["₹", "inr", "rs.", "$"]):
            score += 20
            reasons.append(
                "Compensation amount is not clearly specified."
            )
            suggestions.append(
                "Clearly specify salary or payment amount and payment cycle."
            )
        else:
            score += 5
            reasons.append(
                "Compensation terms are clearly defined."
            )

    # -----------------------------
    # GENERAL CLAUSES
    # -----------------------------

    else:
        score += 5
        reasons.append(
            "General contractual obligation."
        )

    # -----------------------------
    # Ambiguity penalty (cross-cutting)
    # -----------------------------

    if any(term in text for term in vague_terms):
        score += 10
        reasons.append(
            "Uses vague or ambiguous terms that may be interpreted against you."
        )
        suggestions.append(
            "Replace vague terms with measurable or time-bound conditions."
        )

    # -----------------------------
    # FINAL RISK LEVEL (Calibrated)
    # -----------------------------

    if score >= 45:
        risk_level = "High"
    elif score >= 20:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "type": clause_type,
        "risk_level": risk_level,
        "score": score,
        "reasons": reasons,
        "suggestions": (
            suggestions if suggestions else ["No immediate action required."]
        )
    }

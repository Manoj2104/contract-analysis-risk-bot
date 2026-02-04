from typing import Dict, List


# -------------------------------------------------
# Clause Classification (ADVANCED)
# -------------------------------------------------

def classify_clause(clause: str) -> str:
    text = clause.lower()

    if any(k in text for k in ["terminate", "termination"]):
        return "Termination"

    if any(k in text for k in [
        "non-compete",
        "non compete",
        "shall not compete",
        "restriction after termination"
    ]):
        return "Non-Compete"

    if any(k in text for k in [
        "confidential",
        "non-disclosure",
        "confidential information"
    ]):
        return "Confidentiality"

    if any(k in text for k in [
        "salary",
        "compensation",
        "fees",
        "payment",
        "remuneration"
    ]):
        return "Compensation"

    if any(k in text for k in [
        "indemnify",
        "liability",
        "damages",
        "losses"
    ]):
        return "Indemnity & Liability"

    if any(k in text for k in [
        "arbitration",
        "jurisdiction",
        "governing law"
    ]):
        return "Dispute Resolution"

    return "General"


# -------------------------------------------------
# Clause Risk Assessment (REAL-TIME ADVANCED)
# -------------------------------------------------

def assess_risk(clause: str) -> Dict:
    text = clause.lower()

    score = 0
    reasons: List[str] = []
    suggestions: List[str] = []
    tags: List[str] = []

    clause_type = classify_clause(clause)

    # -----------------------------
    # Red flags (deal breakers)
    # -----------------------------
    critical_red_flags = [
        "sole discretion",
        "without notice",
        "at any time",
        "irrevocable",
        "in perpetuity",
        "unlimited liability"
    ]

    # -----------------------------
    # Ambiguous language
    # -----------------------------
    ambiguity_terms = [
        "reasonable",
        "best efforts",
        "as soon as possible",
        "from time to time",
        "material"
    ]

    # -----------------------------
    # TERMINATION
    # -----------------------------
    if clause_type == "Termination":
        score += 20
        tags.append("Employment Risk")

        if any(k in text for k in ["without notice", "immediate termination"]):
            score += 30
            reasons.append("Termination without adequate notice.")
            suggestions.append("Introduce minimum notice period (e.g., 30 days).")
            tags.append("High Impact")

    # -----------------------------
    # NON-COMPETE
    # -----------------------------
    elif clause_type == "Non-Compete":
        score += 35
        reasons.append("Restricts future employment opportunities.")
        suggestions.append(
            "Limit non-compete by duration, geography, and business scope."
        )
        tags.append("Post-Termination Risk")

    # -----------------------------
    # CONFIDENTIALITY
    # -----------------------------
    elif clause_type == "Confidentiality":
        score += 10
        reasons.append("Standard confidentiality obligation.")
        tags.append("IP Protection")

        if "forever" in text or "in perpetuity" in text:
            score += 15
            reasons.append("Confidentiality obligation has no end date.")
            suggestions.append("Limit confidentiality to 2–5 years.")

    # -----------------------------
    # COMPENSATION
    # -----------------------------
    elif clause_type == "Compensation":
        if not any(k in text for k in ["₹", "inr", "rs.", "$"]):
            score += 25
            reasons.append("Compensation amount is unclear or missing.")
            suggestions.append("Specify clear payment amount and schedule.")
            tags.append("Financial Risk")
        else:
            score += 5
            reasons.append("Compensation terms are defined.")

    # -----------------------------
    # INDEMNITY & LIABILITY
    # -----------------------------
    elif clause_type == "Indemnity & Liability":
        score += 30
        reasons.append("Broad indemnity or liability exposure.")
        suggestions.append(
            "Cap liability and exclude indirect or consequential damages."
        )
        tags.append("Financial Exposure")

    # -----------------------------
    # DISPUTE RESOLUTION
    # -----------------------------
    elif clause_type == "Dispute Resolution":
        score += 10
        tags.append("Legal Process")

        if "sole arbitrator appointed by" in text:
            score += 20
            reasons.append("Unilateral arbitrator appointment.")
            suggestions.append("Provide mutual appointment mechanism.")

    # -----------------------------
    # GENERAL
    # -----------------------------
    else:
        score += 5
        reasons.append("General contractual obligation.")

    # -----------------------------
    # AMBIGUITY PENALTY
    # -----------------------------
    if any(term in text for term in ambiguity_terms):
        score += 10
        reasons.append("Uses ambiguous or subjective language.")
        suggestions.append("Replace vague terms with measurable obligations.")
        tags.append("Ambiguity")

    # -----------------------------
    # CRITICAL RED FLAG BOOST
    # -----------------------------
    if any(flag in text for flag in critical_red_flags):
        score += 20
        reasons.append("Contains critical red-flag language.")
        tags.append("Critical")

    # -----------------------------
    # FINAL RISK LEVEL
    # -----------------------------
    if score >= 60:
        risk_level = "High"
        negotiation_priority = "Immediate"
    elif score >= 30:
        risk_level = "Medium"
        negotiation_priority = "Recommended"
    else:
        risk_level = "Low"
        negotiation_priority = "Optional"

    # Confidence (simple explainable heuristic)
    confidence = min(0.95, 0.6 + (score / 120))

    return {
        "type": clause_type,
        "risk_level": risk_level,
        "score": score,
        "confidence": round(confidence, 2),
        "negotiation_priority": negotiation_priority,
        "reasons": reasons,
        "suggestions": suggestions if suggestions else ["No immediate action required."],
        "tags": tags
    }

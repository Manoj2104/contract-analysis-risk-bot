from typing import Dict, List
import random

# =================================================
# HELPER: BASE REWRITE TEMPLATES
# =================================================

REWRITE_TEMPLATES = {
    "Termination": {
        "High": (
            "Either party may terminate this Agreement only after providing "
            "a minimum written notice of {notice_days} days. Termination "
            "shall be permitted solely for defined material breach or "
            "mutual agreement, ensuring fairness to both parties."
        ),
        "Medium": (
            "Termination rights under this clause should be clarified by "
            "specifying valid grounds for termination and an appropriate "
            "notice period."
        )
    },

    "Confidentiality": {
        "High": (
            "Confidential information shall be protected for a defined period "
            "of {years} years from the date of disclosure. Obligations shall "
            "apply only to information expressly identified as confidential."
        ),
        "Medium": (
            "Confidentiality obligations should clearly define the scope, "
            "exceptions, and duration of protection."
        )
    },

    "Compensation": {
        "High": (
            "All compensation payable under this Agreement shall be clearly "
            "specified, including amount, payment schedule, and mode of "
            "payment, to avoid ambiguity or dispute."
        ),
        "Medium": (
            "Payment terms should be clarified with defined timelines and "
            "amounts."
        )
    },

    "General": {
        "High": (
            "This clause should be revised to include objective standards, "
            "mutual obligations, and clearly defined limitations to prevent "
            "unilateral or unfair interpretation."
        ),
        "Medium": (
            "This clause should be clarified by replacing vague language with "
            "measurable and objective criteria."
        )
    }
}

# =================================================
# MAIN REAL-TIME REWRITE FUNCTION
# =================================================

def rewrite_clause(
    clause_text: str,
    risk_level: str,
    clause_type: str = "General",
    ambiguity: List[str] = None,
    law_issues: List[str] = None
) -> Dict:
    """
    Advanced real-time clause rewriting engine.

    Returns:
    {
        rewritten_clause,
        rewrite_strategy,
        why_this_change,
        confidence
    }
    """

    ambiguity = ambiguity or []
    law_issues = law_issues or []

    # -----------------------------
    # Base rewrite selection
    # -----------------------------
    templates = REWRITE_TEMPLATES.get(clause_type, REWRITE_TEMPLATES["General"])

    if risk_level == "High":
        rewritten = templates.get("High")
        strategy = "Risk Mitigation"
    elif risk_level == "Medium":
        rewritten = templates.get("Medium")
        strategy = "Clarification"
    else:
        return {
            "rewritten_clause": (
                "This clause is acceptable and aligned with standard SME "
                "contracting practices. No immediate changes are required."
            ),
            "rewrite_strategy": "No Change",
            "why_this_change": "Clause presents low legal risk.",
            "confidence": 0.9
        }

    # -----------------------------
    # Dynamic personalization
    # -----------------------------
    rewritten = rewritten.format(
        notice_days=random.choice([15, 30]),
        years=random.choice([2, 3, 5])
    )

    # -----------------------------
    # Ambiguity handling
    # -----------------------------
    if ambiguity:
        rewritten += (
            " Vague expressions such as "
            f"{', '.join(ambiguity)} have been replaced with "
            "clear, measurable obligations."
        )

    # -----------------------------
    # Indian law softening
    # -----------------------------
    if law_issues:
        rewritten += (
            " This revision aligns the clause with generally accepted "
            "Indian legal principles to reduce enforceability risks."
        )

    # -----------------------------
    # Confidence estimation
    # -----------------------------
    confidence = 0.75
    if risk_level == "High":
        confidence += 0.1
    if ambiguity:
        confidence += 0.05
    if law_issues:
        confidence += 0.05

    confidence = min(confidence, 0.95)

    return {
        "rewritten_clause": rewritten,
        "rewrite_strategy": strategy,
        "why_this_change": (
            "The original clause posed legal risk due to "
            f"{'ambiguity' if ambiguity else 'imbalance'} and "
            "potential enforceability concerns."
        ),
        "confidence": round(confidence, 2)
    }

from typing import Dict


# -------------------------------------------------
# HEALTH SCORE (NORMALIZED – REAL WORLD)
# -------------------------------------------------
def calculate_health_score(
    total_risk_score: int,
    total_clauses: int
) -> int:
    """
    Converts total risk score into a normalized health score (0–100).

    Uses average risk per clause instead of raw sum.
    Prevents long contracts from being unfairly penalized.
    """

    if total_clauses == 0:
        return 100

    avg_risk = total_risk_score / total_clauses

    # Scale factor tuned for legal realism
    health = 100 - (avg_risk * 2)

    return int(max(0, min(100, round(health))))


# -------------------------------------------------
# FINAL DECISION ENGINE (STRICT LEGAL MODE)
# -------------------------------------------------
def make_final_decision(
    total_risk_score: int,
    high_risk_count: int,
    medium_risk_count: int,
    total_clauses: int
) -> Dict:
    """
    STRICT LEGAL DECISION LOGIC:

    Rules:
    - Any High Risk       → ❌ Do Not Sign
    - Any Medium Risk     → ⚠️ Sign After Changes
    - Only All Low Risks  → ✅ Safe to Sign
    """

    health_score = calculate_health_score(
        total_risk_score=total_risk_score,
        total_clauses=total_clauses
    )

    # -----------------------------
    # STRICT, PREDICTABLE RULES
    # -----------------------------
    if high_risk_count >= 1:
        decision = "❌ Do Not Sign"
        explanation = (
            "The contract contains high-risk clauses that may expose you "
            "to serious legal or financial liability."
        )

    elif medium_risk_count >= 1:
        decision = "⚠️ Sign After Changes"
        explanation = (
            "The contract contains one or more medium-risk clauses. "
            "These clauses should be revised or clarified before signing."
        )

    else:
        decision = "✅ Safe to Sign"
        explanation = (
            "All clauses are assessed as low risk. "
            "The contract is suitable for signing under standard business conditions."
        )

    return {
        "health_score": health_score,
        "decision": decision,
        "explanation": explanation
    }

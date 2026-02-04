from typing import List


def generate_executive_summary(
    contract_type: str,
    high_risk_count: int,
    medium_risk_count: int,
    missing_clauses: List[str],
    decision: str
) -> List[str]:
    """
    Returns structured executive summary lines
    grouped by importance.
    """

    lines = []

    # Contract info
    lines.append(f"📄 Contract Type: {contract_type}")

    # Risk findings
    if high_risk_count > 0:
        lines.append(f"⚠️ {high_risk_count} high-risk clause(s) identified that may significantly impact you.")

    if medium_risk_count > 0:
        lines.append(f"🟡 {medium_risk_count} medium-risk clause(s) require careful review.")

    if missing_clauses:
        lines.append("❗ Some important clauses are missing, which may expose you to legal uncertainty.")

    # Recommendation (keep separate)
    lines.append(f"RECOMMENDATION::{decision}")

    return lines

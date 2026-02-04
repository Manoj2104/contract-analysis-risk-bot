def get_risk_tags(clause_type: str, risk_level: str) -> list:
    tags = []

    if clause_type == "Termination":
        tags.append("🔴 Termination Risk")

    if clause_type == "Non-Compete":
        tags.append("🟠 Employment Restriction")

    if clause_type == "Compensation":
        tags.append("🟢 Financial Clarity")

    if clause_type == "Confidentiality":
        tags.append("🔵 Information Protection")

    if risk_level == "High":
        tags.append("⚠️ High Legal Exposure")

    return tags

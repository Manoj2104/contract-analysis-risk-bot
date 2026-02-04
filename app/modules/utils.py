def generate_insights(df, entities):
   

    insights = []

    # -----------------------------
    # Safety checks
    # -----------------------------
    if df is None or df.empty:
        return ["No clauses available for analysis."]

    entities = entities or {}

    # -----------------------------
    # High-risk clause detection
    # -----------------------------
    if "Risk" in df.columns:
        if (df["Risk"].astype(str).str.lower() == "high").any():
            insights.append(
                "High-risk clauses detected. Immediate legal review is strongly recommended."
            )

    # -----------------------------
    # Non-compete clause warning
    # -----------------------------
    if "Type" in df.columns:
        if df["Type"].astype(str).str.contains("non[- ]?compete", case=False).any():
            insights.append(
                "Non-compete clauses detected. These may restrict future employment or business opportunities."
            )

    # -----------------------------
    # Financial exposure insight
    # -----------------------------
    money_entities = entities.get("MONEY", [])
    if isinstance(money_entities, (list, tuple)) and money_entities:
        insights.append(
            f"Financial amounts referenced in the contract: {', '.join(map(str, money_entities))}."
        )

    # -----------------------------
    # Fallback insight
    # -----------------------------
    if not insights:
        insights.append(
            "No critical legal risks detected. The contract appears balanced based on automated analysis."
        )

    return insights

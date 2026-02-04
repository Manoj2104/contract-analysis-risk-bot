from typing import Dict
import pandas as pd


def aggregate_contract_risk(df: pd.DataFrame) -> Dict:
    """
    Aggregates risk across all clauses using legally realistic weighting.

    INPUT (FINAL PIPELINE):
    DataFrame with columns:
    - Clause ID
    - Risk       (Low / Medium / High)
    - Score      (numeric)

    RETURNS:
    {
        total_risk_score: int,
        high_risk_count: int,
        medium_risk_count: int,
        low_risk_count: int
    }
    """

    # -----------------------------
    # SAFETY CHECKS (CRITICAL)
    # -----------------------------
    if df is None or df.empty:
        return {
            "total_risk_score": 0,
            "high_risk_count": 0,
            "medium_risk_count": 0,
            "low_risk_count": 0
        }

    total_risk_score = 0
    high = 0
    medium = 0
    low = 0

    # -----------------------------
    # WEIGHTED LEGAL AGGREGATION
    # -----------------------------
    for _, row in df.iterrows():

        risk = row.get("Risk", "Low")
        score = int(row.get("Score", 0))

        if risk == "High":
            high += 1
            total_risk_score += 40   # 🔴 heavy legal impact
        elif risk == "Medium":
            medium += 1
            total_risk_score += 15   # 🟠 moderate impact
        else:
            low += 1
            total_risk_score += 2    # 🟢 minimal impact

    return {
        "total_risk_score": total_risk_score,
        "high_risk_count": high,
        "medium_risk_count": medium,
        "low_risk_count": low
    }

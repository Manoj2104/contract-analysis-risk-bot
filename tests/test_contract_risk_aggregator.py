import os
import sys
import pytest

# Fix Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.contract_risk_aggregator import aggregate_contract_risk


def test_aggregate_multiple_clauses():
    clauses = [
        {
            "clause_id": 1,
            "text": "The employer may terminate the employee at any time without notice."
        },
        {
            "clause_id": 2,
            "text": "The employee shall not compete with the employer for two years."
        },
        {
            "clause_id": 3,
            "text": "The employee shall receive a salary of ₹50,000 per month."
        }
    ]

    result = aggregate_contract_risk(clauses)

    assert result["total_risk_score"] > 0
    assert result["high_risk_count"] >= 1
    assert result["medium_risk_count"] >= 0
    assert result["low_risk_count"] >= 0
    assert len(result["clause_results"]) == 3


def test_empty_clauses_safe():
    result = aggregate_contract_risk([])

    assert result["total_risk_score"] == 0
    assert result["high_risk_count"] == 0
    assert result["medium_risk_count"] == 0
    assert result["low_risk_count"] == 0
    assert result["clause_results"] == []

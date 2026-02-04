import os
import sys
import pytest

# Fix Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.decision_engine import (
    calculate_health_score,
    make_final_decision
)


def test_health_score_calculation():
    assert calculate_health_score(0) == 100
    assert calculate_health_score(30) == 70
    assert calculate_health_score(120) == 0


def test_safe_to_sign_decision():
    result = make_final_decision(
        total_risk_score=20,
        high_risk_count=0
    )

    assert result["decision"] == "✅ Safe to Sign"
    assert result["health_score"] >= 75


def test_sign_after_changes_decision():
    result = make_final_decision(
        total_risk_score=45,
        high_risk_count=1
    )

    assert result["decision"] == "⚠️ Sign After Changes"
    assert 50 <= result["health_score"] < 75


def test_do_not_sign_decision():
    result = make_final_decision(
        total_risk_score=80,
        high_risk_count=2
    )

    assert result["decision"] == "❌ Do Not Sign"
    assert result["health_score"] < 50

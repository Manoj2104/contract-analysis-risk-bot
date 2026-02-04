import os
import sys
import pytest

# -------------------------------------------------
# Fix Python path (same pattern used everywhere)
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.clause_risk import classify_clause, assess_risk

# ⚠️ If these functions are in a DIFFERENT file,
# change the import accordingly:
# from app.modules.<your_file_name> import classify_clause, assess_risk


# -------------------------------------------------
# Tests for classify_clause
# -------------------------------------------------

def test_classify_termination_clause():
    clause = "The employer may terminate the employee without notice."
    assert classify_clause(clause) == "Termination"


def test_classify_non_compete_clause():
    clause = "The employee shall not engage in competing businesses."
    assert classify_clause(clause) == "Non-Compete"


def test_classify_confidentiality_clause():
    clause = "All confidential information must be protected."
    assert classify_clause(clause) == "Confidentiality"


def test_classify_compensation_clause():
    clause = "The salary shall be INR 50,000 per month."
    assert classify_clause(clause) == "Compensation"


def test_classify_general_clause():
    clause = "This agreement is made between the parties."
    assert classify_clause(clause) == "General"


# -------------------------------------------------
# Tests for assess_risk
# -------------------------------------------------

def test_high_risk_termination_clause():
    clause = "The employer may terminate the employee at any time without notice."
    result = assess_risk(clause)

    assert result["type"] == "Termination"
    assert result["risk_level"] == "High"
    assert result["score"] >= 40
    assert len(result["reasons"]) > 0
    assert len(result["suggestions"]) > 0


def test_medium_risk_non_compete_clause():
    clause = "The employee shall not compete with the employer for two years."
    result = assess_risk(clause)

    assert result["type"] == "Non-Compete"
    assert result["risk_level"] in ["Medium", "High"]
    assert result["score"] > 0


def test_low_risk_confidentiality_clause():
    clause = "The employee shall keep confidential information private."
    result = assess_risk(clause)

    assert result["type"] == "Confidentiality"
    assert result["risk_level"] == "Low"
    assert result["score"] > 0


def test_compensation_without_amount():
    clause = "The employee shall receive compensation as agreed."
    result = assess_risk(clause)

    assert result["type"] == "Compensation"
    assert result["risk_level"] in ["Medium", "High"]
    assert "not clearly specified" in " ".join(result["reasons"]).lower()


def test_compensation_with_amount():
    clause = "The employee shall receive a salary of ₹40,000 per month."
    result = assess_risk(clause)

    assert result["type"] == "Compensation"
    assert result["risk_level"] == "Low"


def test_ambiguity_penalty_applied():
    clause = "The vendor shall use reasonable efforts to deliver services."
    result = assess_risk(clause)

    assert result["score"] >= 10
    assert any(
        "ambiguous" in reason.lower()
        for reason in result["reasons"]
    )


def test_empty_clause_safe_handling():
    result = assess_risk("")

    assert result["risk_level"] == "Low"
    assert result["score"] >= 0

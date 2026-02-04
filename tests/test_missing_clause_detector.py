import os
import sys
import pytest

# -------------------------------------------------
# Fix Python path
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.missing_clause_detector import detect_missing_clauses


def test_detects_missing_clauses():
    text = "The Vendor shall deliver goods and raise invoices accordingly."
    missing = detect_missing_clauses(text)

    assert "Termination" in missing
    assert "Jurisdiction" in missing


def test_no_missing_clauses_when_all_present():
    text = """
    This Agreement may be terminated by either party.
    Payment shall be made within 30 days.
    Governing law shall be the laws of India.
    Confidential information shall not be disclosed.
    Liability shall be limited to the contract value.
    """
    missing = detect_missing_clauses(text)

    assert missing == []


def test_empty_contract_text():
    missing = detect_missing_clauses("")

    assert len(missing) > 0

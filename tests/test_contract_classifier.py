import os
import sys
import pytest

# -------------------------------------------------
# Fix Python path (same pattern as other tests)
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.contract_classifier import classify_contract


def test_employment_contract_classification():
    text = "The Employee shall receive a salary and shall follow company policies."
    contract_type, confidence = classify_contract(text)

    assert contract_type == "Employment Agreement"
    assert confidence > 0.0


def test_vendor_contract_classification():
    text = "The Vendor shall deliver goods and raise invoices accordingly."
    contract_type, confidence = classify_contract(text)

    assert contract_type == "Vendor Contract"
    assert confidence > 0.0


def test_nda_contract_classification():
    text = "This Agreement contains confidential information and is a non-disclosure agreement."
    contract_type, confidence = classify_contract(text)

    assert contract_type == "NDA"
    assert confidence > 0.0


def test_unknown_contract_fallback():
    text = "This document describes general terms without legal keywords."
    contract_type, confidence = classify_contract(text)

    assert contract_type in ["General Contract", "Unknown"]
    assert confidence >= 0.0


def test_empty_text_handling():
    contract_type, confidence = classify_contract("")

    assert contract_type in ["Unknown", "General Contract"]
    assert confidence >= 0.0

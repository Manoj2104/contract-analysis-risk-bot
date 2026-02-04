import os
import sys
import pytest

# Fix Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.ambiguity_detector import detect_ambiguity


def test_detects_single_ambiguous_term():
    clause = "The Vendor shall use reasonable efforts to deliver the goods."
    terms = detect_ambiguity(clause)

    assert "reasonable" in terms


def test_detects_multiple_ambiguous_terms():
    clause = (
        "The Service Provider shall use best efforts and act in a commercially "
        "reasonable manner from time to time."
    )
    terms = detect_ambiguity(clause)

    assert "best efforts" in terms
    assert "commercially reasonable" in terms
    assert "from time to time" in terms


def test_no_ambiguity_detected():
    clause = "The Vendor shall deliver the goods within 30 days."
    terms = detect_ambiguity(clause)

    assert terms == []


def test_empty_clause():
    terms = detect_ambiguity("")
    assert terms == []

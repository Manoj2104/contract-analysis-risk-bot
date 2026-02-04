import os
import sys
import pytest

# Fix Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.obligation_tagger import tag_clause_type


def test_obligation_detection():
    clause = "The Vendor shall deliver the goods within 30 days."
    assert tag_clause_type(clause) == "Obligation"


def test_prohibition_detection():
    clause = "The Employee shall not disclose confidential information."
    assert tag_clause_type(clause) == "Prohibition"


def test_right_detection():
    clause = "The Client may terminate the agreement with prior notice."
    assert tag_clause_type(clause) == "Right"


def test_neutral_clause():
    clause = "This Agreement is made between the parties."
    assert tag_clause_type(clause) == "Neutral"


def test_empty_text():
    assert tag_clause_type("") == "Neutral"

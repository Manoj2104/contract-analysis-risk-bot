import os
import sys
import pytest

# -------------------------------------------------
# FIX PYTHON PATH (IMPORTANT)
# -------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from app.modules.clause_extractor import extract_clauses


# ---------- Helpers ----------

def load_sample_contract():
    """
    Loads the sample contract text from data/samples
    """
    sample_path = os.path.join(
        PROJECT_ROOT, "data", "samples", "sample_contract.txt"
    )

    assert os.path.exists(sample_path), "❌ sample_contract.txt not found"

    with open(sample_path, "r", encoding="utf-8") as f:
        return f.read()


# ---------- Tests ----------

def test_clause_extraction_returns_list():
    text = load_sample_contract()
    clauses = extract_clauses(text)

    assert isinstance(clauses, list), "Clauses should be returned as a list"


def test_clause_extraction_not_empty():
    text = load_sample_contract()
    clauses = extract_clauses(text)

    assert len(clauses) > 0, "No clauses extracted from sample contract"


def test_clause_structure():
    text = load_sample_contract()
    clauses = extract_clauses(text)

    clause = clauses[0]

    assert isinstance(clause, dict), "Each clause must be a dictionary"
    assert "clause_id" in clause, "Missing clause_id"
    assert "text" in clause, "Missing clause text"
    assert "title" in clause, "Missing clause title key"


def test_clause_text_quality():
    text = load_sample_contract()
    clauses = extract_clauses(text)

    for clause in clauses:
        assert len(clause["text"]) >= 50, (
            f"Clause too short: {clause['text']}"
        )


def test_clause_id_sequence():
    text = load_sample_contract()
    clauses = extract_clauses(text)

    ids = [c["clause_id"] for c in clauses]
    assert ids == list(range(1, len(ids) + 1)), "Clause IDs must be sequential"


def test_heading_detection_optional():
    """
    Title can be None or a valid heading (UPPERCASE).
    """
    text = load_sample_contract()
    clauses = extract_clauses(text)

    for clause in clauses:
        title = clause["title"]
        if title:
            assert title.isupper(), "Clause title should be uppercase"

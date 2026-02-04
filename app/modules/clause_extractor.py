import re
from typing import List, Dict

# =================================================
# TEXT CLEANING
# =================================================

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\t", " ")
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ ]{2,}", " ", text)

    return text.strip()


# =================================================
# HEADING DETECTOR
# =================================================

def _is_heading(line: str) -> bool:
    line = line.strip()
    return line.isupper() and 5 < len(line) <= 60


# =================================================
# CLAUSE TYPE GUESS (EMPLOYMENT + LEASE AWARE)
# =================================================

def guess_clause_type(text: str) -> str:
    t = text.lower()

    # ---------------- SECURITY / DEPOSIT ----------------
    if re.search(r"security deposit|advance deposit|refundable|refund", t):
        return "Security Deposit & Refund"

    # ---------------- PAYMENT / SALARY / RENT ----------------
    if re.search(
        r"salary|wages|rent|payable|payment|electricity|charges|meter reading|rupees|₹",
        t
    ):
        return "Payment & Financial Terms"

    # ---------------- MAINTENANCE / HANDOVER ----------------
    if re.search(
        r"maintain|maintenance|good condition|repair|restore|handing over|"
        r"vacant possession|deliver the premises",
        t
    ):
        return "Maintenance & Handover"

    # ---------------- USE / RESTRICTIONS ----------------
    if re.search(
        r"residential purpose|not sub-let|sublet|illegal activities|"
        r"alteration|additional fittings|structures",
        t
    ):
        return "Use of Premises & Restrictions"

    # ---------------- TERMINATION ----------------
    if re.search(
        r"terminate|termination|dismiss|evicted|eviction|without notice|"
        r"may terminate at any time",
        t
    ):
        return "Termination"

    # ---------------- NOTICE ----------------
    if re.search(
        r"notice|vacating|vacate|vacation|required to give|"
        r"three months notice|90 days notice|30 days notice",
        t
    ):
        return "Notice & Possession"

    # ---------------- NON-COMPETE ----------------
    if re.search(r"non[- ]?compete|restriction after termination", t):
        return "Non-Compete"

    # ---------------- CONFIDENTIALITY ----------------
    if re.search(r"confidential|non-disclosure|nda", t):
        return "Confidentiality"

    # ---------------- INDEMNITY / LIABILITY ----------------
    if re.search(r"indemnify|indemnity|hold harmless|liable", t):
        return "Indemnity & Liability"

    # ---------------- GOVERNING LAW ----------------
    if re.search(r"governing law|jurisdiction|courts at", t):
        return "Governing Law & Jurisdiction"

    # ---------------- FORCE MAJEURE ----------------
    if re.search(r"force majeure|act of god", t):
        return "Force Majeure"

    return "General"


# =================================================
# QUALITY ANALYSIS
# =================================================

def analyze_clause_quality(text: str) -> Dict:
    length = len(text)
    sentences = len(re.findall(r"[.!?]", text))

    warnings = []

    if length < 50:
        warnings.append("Clause is unusually short")
    if length > 1200:
        warnings.append("Clause is unusually long (possible merge)")
    if sentences == 0:
        warnings.append("No sentence structure detected")

    quality_score = max(
        0.4,
        min(1.0, (sentences / 5) + (length / 800))
    )

    return {
        "length": length,
        "sentences": sentences,
        "quality_score": round(quality_score, 2),
        "warnings": warnings
    }


# =================================================
# ACTION DECISION
# =================================================

def decide_action(quality: Dict) -> str:
    if quality["warnings"]:
        return "Review Required"
    if quality["quality_score"] < 0.6:
        return "Rewrite Suggested"
    return "Looks Acceptable"

def is_ocr_noise(text: str) -> bool:
    noise_patterns = [
        "stamp vendor",
        "page",
        "witness",
        "hands and seal",
        "executed at",
        "rental agreement",
        "chettinad",
        "registration no",
        "govt of tamilnadu"
    ]

    text = text.lower()
    if len(text.strip()) < 40:
        return True

    return any(pat in text for pat in noise_patterns)

# =================================================
# MAIN CLAUSE EXTRACTION ENGINE
# =================================================
def extract_clauses(text: str) -> List[Dict]:
    """
    FINAL PROFESSIONAL CLAUSE ENGINE
    + Smart paragraph splitter for single-block contracts
    """

    text = clean_text(text)
    lines = text.split("\n")

    clauses = []
    current = []
    title = None
    clause_id = 1
    source = "paragraph"

    number_pattern = re.compile(r"^\d+(\.\d+)*[\)\.]?\s+")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # -------- HEADING --------
        if _is_heading(line):
            if current:
                clause_text = " ".join(current)
                quality = analyze_clause_quality(clause_text)

                clauses.append({
                    "clause_id": clause_id,
                    "title": title,
                    "text": clause_text,
                    "type_hint": guess_clause_type(clause_text),
                    "quality": quality,
                    "action": decide_action(quality),
                    "source": source
                })
                clause_id += 1
                current = []

            title = line
            source = "heading"
            continue

        # -------- NUMBERED --------
        if number_pattern.match(line):
            if current:
                clause_text = " ".join(current)
                quality = analyze_clause_quality(clause_text)

                clauses.append({
                    "clause_id": clause_id,
                    "title": title,
                    "text": clause_text,
                    "type_hint": guess_clause_type(clause_text),
                    "quality": quality,
                    "action": decide_action(quality),
                    "source": source
                })
                clause_id += 1

            current = [line]
            title = None
            source = "numbered"
            continue

        current.append(line)

    # -------- LAST BLOCK --------
    if current:
        clause_text = " ".join(current)
        quality = analyze_clause_quality(clause_text)

        clauses.append({
            "clause_id": clause_id,
            "title": title,
            "text": clause_text,
            "type_hint": guess_clause_type(clause_text),
            "quality": quality,
            "action": decide_action(quality),
            "source": source
        })

    # =================================================
    # 🚨 SMART FALLBACK: SENTENCE-LEVEL SPLIT
    # =================================================
    if len(clauses) == 1:
        block = clauses[0]["text"]

        # legal sentence triggers
        sentences = re.split(
            r"(?i)(?<=\.)\s+(?=the\s+(employee|employer)|"
            r"employee\s+shall|employer\s+may|shall\s+receive|shall\s+not)",
            block
        )

        if len(sentences) >= 3:
            new_clauses = []
            for idx, s in enumerate(sentences, 1):
                s = s.strip()
                if len(s) < 40:
                    continue

                quality = analyze_clause_quality(s)

                new_clauses.append({
                    "clause_id": idx,
                    "title": None,
                    "text": s,
                    "type_hint": guess_clause_type(s),
                    "quality": quality,
                    "action": decide_action(quality),
                    "source": "sentence-split"
                })

            if len(new_clauses) > 1:
                return new_clauses
            # =================================================
        # 🚨 OCR / DEGRADED TEXT FALLBACK (CRITICAL)
        # =================================================
        if len(clauses) <= 1:
            block = text.strip()

            rough_sentences = re.split(
                r"(?<=[\.\!\?])\s+|[\n•\-–—]+",
                block
            )

            rebuilt = []
            cid = 1

            for s in rough_sentences:
                s = s.strip()

                # Skip noise
                if len(s) < 25:
                    continue

                quality = analyze_clause_quality(s)

                rebuilt.append({
                    "clause_id": cid,
                    "title": None,
                    "text": s,
                    "type_hint": guess_clause_type(s),
                    "quality": quality,
                    "action": decide_action(quality),
                    "source": "ocr-fallback"
                })

                cid += 1

            if len(rebuilt) >= 3:
                return rebuilt

        

    return clauses

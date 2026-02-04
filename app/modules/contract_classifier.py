from collections import defaultdict
from typing import Tuple, Dict, List

# =================================================
# ADVANCED CONTRACT KEYWORD RULES (HARDENED)
# =================================================

CONTRACT_RULES: Dict[str, Dict] = {
    "Employment Agreement": {
        "positive": {
            "employee": 3,
            "employer": 3,
            "salary": 3,
            "wages": 3,
            "notice period": 2,
            "termination": 2,
            "probation": 2,
            "appointment": 1,
            "working hours": 1,
            "leave": 1
        },
        "negative": [
            "rent", "lease", "lessor", "lessee",
            "security deposit", "premises"
        ]
    },

    "Vendor Contract": {
        "positive": {
            "vendor": 3,
            "supplier": 3,
            "purchase order": 2,
            "invoice": 2,
            "delivery": 2,
            "goods": 1
        },
        "negative": [
            "employee", "salary", "probation"
        ]
    },

    "Service Agreement": {
        "positive": {
            "services": 3,
            "scope of work": 3,
            "milestones": 2,
            "fees": 2,
            "service level": 2,
            "performance": 1
        },
        "negative": [
            "rent", "lease", "salary"
        ]
    },

    "Lease Agreement": {
        "positive": {
            "lease": 3,
            "rent": 3,
            "lessor": 3,
            "lessee": 3,
            "premises": 2,
            "security deposit": 2,
            "tenure": 1,
            "lock-in": 1,
            "vacate": 1
        },
        "negative": [
            "employee", "salary", "probation",
            "appointment", "wages"
        ]
    },

    "NDA": {
        "positive": {
            "confidential": 3,
            "non-disclosure": 3,
            "confidential information": 2,
            "trade secret": 2,
            "disclosure": 1
        },
        "negative": [
            "salary", "rent", "invoice", "lease"
        ]
    }
}

# =================================================
# OCR / NOISE FILTER
# =================================================

NOISE_PATTERNS = [
    "stamp vendor",
    "rental agreement",
    "hands and seal",
    "witness",
    "page",
    "dated",
    "executed at"
]

# =================================================
# INTERNAL HELPERS
# =================================================

def _normalize_confidence(raw: float) -> float:
    """
    Smooths confidence so results feel realistic.
    """
    raw = max(raw, 0)
    if raw < 0.45:
        return 0.45
    if raw > 0.95:
        return 0.95
    return round(raw, 2)


def explain_classification(text: str, contract_type: str) -> List[str]:
    """
    Returns human-readable reasons for classification.
    """
    text = text.lower()
    reasons = []

    rules = CONTRACT_RULES.get(contract_type)
    if not rules:
        return ["Generic contractual structure detected."]

    for kw, weight in rules["positive"].items():
        if kw in text:
            reasons.append(
                f"Keyword '{kw}' indicates {contract_type} (weight {weight})."
            )

    if not reasons:
        reasons.append(
            "Overall contractual language pattern matches this agreement type."
        )

    return reasons[:5]

# =================================================
# CONTRACT CLASSIFIER (ENTERPRISE SAFE)
# =================================================

def classify_contract(text: str) -> Tuple[str, float]:
    """
    Advanced rule-based contract classification (LEASE-SAFE + OCR-SAFE)

    Returns:
    (contract_type, confidence_score)
    """

    if not text or len(text.strip()) < 100:
        return "General Contract", 0.45

    text = text.lower()

    # ---------------------------------------------
    # Remove OCR noise influence
    # ---------------------------------------------
    for noise in NOISE_PATTERNS:
        text = text.replace(noise, "")

    # ---------------------------------------------
    # HARD LEASE OVERRIDE (CRITICAL FIX)
    # ---------------------------------------------
    lease_markers = [
        "rent",
        "lease",
        "lessor",
        "lessee",
        "tenant",
        "house owner",
        "premises",
        "security deposit",
        "advance deposit",
        "vacating",
        "monthly rent"
    ]

    lease_hits = sum(1 for kw in lease_markers if kw in text)

    if lease_hits >= 4:
        # Clear rental agreement → do NOT dilute confidence
        return "Lease Agreement", 0.85

    # ---------------------------------------------
    # Normal scoring (fallback)
    # ---------------------------------------------
    scores = defaultdict(int)
    max_scores = {}

    for contract_type, rules in CONTRACT_RULES.items():
        max_scores[contract_type] = sum(rules["positive"].values())

        # Positive scoring
        for kw, weight in rules["positive"].items():
            if kw in text:
                scores[contract_type] += weight

        # Strong negative penalties
        for neg_kw in rules.get("negative", []):
            if neg_kw in text:
                scores[contract_type] -= 2

    # ---------------------------------------------
    # Weak / generic detection
    # ---------------------------------------------
    best_score = max(scores.values(), default=0)
    if best_score < 3:
        return "General Contract", 0.5

    # ---------------------------------------------
    # Rank contract types
    # ---------------------------------------------
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_type, best_score = ranked[0]
    second_type, second_score = ranked[1] if len(ranked) > 1 else (None, 0)

    # ---------------------------------------------
    # Multi-contract detection (STRICT)
    # ---------------------------------------------
    if (
        second_type
        and second_score >= best_score * 0.8
        and second_score >= 4
    ):
        contract_type = f"{best_type} + {second_type}"
        raw_confidence = (
            best_score + second_score
        ) / (
            max_scores[best_type]
            + max_scores.get(second_type, 1)
        )
    else:
        contract_type = best_type
        raw_confidence = best_score / max_scores[best_type]

    # ---------------------------------------------
    # Confidence normalization (LEGAL-SAFE)
    # ---------------------------------------------
    confidence = max(0.7, min(_normalize_confidence(raw_confidence), 0.95))

    return contract_type, confidence


def normalize_clause_type_advanced(text: str, base_type: str) -> str:
    """
    Advanced semantic normalizer for ALL contract types.
    """

    if not text:
        return base_type

    t = text.lower().strip()
    length = len(t)

    # -------------------------------------------------
    # HARD EXIT — VERY SHORT / OCR NOISE
    # -------------------------------------------------
    if length < 60:
        return base_type

    # -------------------------------------------------
    # STRONG OPERATIONAL SIGNALS (LOCKED)
    # -------------------------------------------------
    HARD_LOCK_TYPES = {
        "Termination": [
            "terminate", "termination", "evict", "dismiss",
            "without notice", "immediate effect"
        ],
        "Payment & Financial Terms": [
            "rs.", "₹", "salary", "rent", "fees",
            "security deposit", "advance amount",
            "increase", "interest"
        ],
        "Confidentiality & NDA": [
            "confidential", "non disclosure", "secret"
        ],
        "Non-Compete / Restrictive Covenant": [
            "non compete", "shall not work",
            "after termination", "for years"
        ],
        "Liability & Indemnity": [
            "indemnify", "liability", "no maximum limit",
            "unlimited liability"
        ],
        "Maintenance & Repairs": [
            "repair", "maintenance", "wear and tear"
        ],
        "Use Restrictions": [
            "residential purpose only",
            "commercial use prohibited"
        ],
        "Inspection & Access Rights": [
            "inspect", "inspection", "access at reasonable"
        ]
    }

    for ctype, signals in HARD_LOCK_TYPES.items():
        if any(k in t for k in signals):
            return ctype

    return base_type

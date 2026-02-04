CRITICAL = ["Jurisdiction", "Termination"]
IMPORTANT = ["Arbitration", "Limitation of Liability"]
OPTIONAL = ["Force Majeure"]


def classify_missing_clauses(missing_clauses: list) -> dict:
    result = {
        "Critical": [],
        "Important": [],
        "Optional": []
    }

    for clause in missing_clauses:
        if clause in CRITICAL:
            result["Critical"].append(clause)
        elif clause in IMPORTANT:
            result["Important"].append(clause)
        else:
            result["Optional"].append(clause)

    return result

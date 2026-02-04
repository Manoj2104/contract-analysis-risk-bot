def simplify_reason(reason: str) -> str:
    return (
        reason
        .replace("termination", "job ending")
        .replace("non-compete", "work restriction")
        .replace("confidentiality", "information sharing")
        .replace("liability", "financial responsibility")
    )

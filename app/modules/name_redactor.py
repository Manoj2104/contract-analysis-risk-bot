import re
from typing import Tuple, Dict

# Common Indian name prefixes
NAME_PREFIXES = r"(mr|mrs|ms|miss|dr|shri|sri)\.?\s+"

def redact_person_names(text: str) -> Tuple[str, Dict[str, str]]:
    """
    Redacts ONLY person names from legal contracts.
    
    Returns:
    - redacted_text
    - mapping of redacted tokens -> original names
    """

    if not text:
        return text, {}

    redaction_map = {}
    counter = 1

    # Pattern: Mr. NAME / Mrs NAME / Dr NAME etc.
    pattern = re.compile(
        rf"{NAME_PREFIXES}([A-Z][a-zA-Z\. ]{{2,40}})",
        flags=re.IGNORECASE
    )

    def replace(match):
        nonlocal counter
        original = match.group(0).strip()

        token = f"[REDACTED_PERSON_{counter}]"
        redaction_map[token] = original
        counter += 1

        return token

    redacted_text = pattern.sub(replace, text)

    return redacted_text, redaction_map

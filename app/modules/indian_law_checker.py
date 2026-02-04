import re
from typing import List


def check_indian_law_issues(
    clause_text: str,
    contract_type: str = "General"
) -> List[str]:
    """
    FINAL Indian Law Checker – Noise-Free & Contract-Aware

    ✔ All contract types
    ✔ Clause-impact filtered
    ✔ No admin / stamp / party noise
    ✔ Real legal-tool behaviour
    """

    issues = []
    text = clause_text.lower()
    ct = contract_type.lower()

    # =================================================
    # 🛑 HARD SKIP – NON-OPERATIVE CLAUSES
    # =================================================
    if re.search(
        r"stamp|witness|seal|signature|page \d|hereinafter|residing at|between mr|address|dated|day of",
        text
    ):
        return []

    # =================================================
    # 🔴 TERMINATION / EVICTION (LEGAL IMPACT)
    # =================================================
    if re.search(r"terminate|termination|evict|eviction", text):

        if "notice" not in text:
            if "lease" in ct or "rent" in ct:
                issues.append(
                    "Eviction or termination without reasonable notice may violate Rent Control principles."
                )
            elif "employment" in ct or "service" in ct:
                issues.append(
                    "Termination without notice may be considered unfair under Indian labour law."
                )
            else:
                issues.append(
                    "Termination without notice may be challenged under Indian contract law."
                )

        if re.search(r"immediate termination", text) and not re.search(
            r"misconduct|fraud|material breach", text
        ):
            issues.append(
                "Immediate termination without defined misconduct may be legally challenged."
            )

    # =================================================
    # 🟡 EMPLOYMENT / SERVICE CONTRACTS
    # =================================================
    if "employment" in ct or "service" in ct:

        if re.search(r"forced resignation|resign upon request", text):
            issues.append(
                "Forced resignation clauses may be treated as illegal termination under Indian law."
            )

        if re.search(r"probation", text) and "sole discretion" in text:
            issues.append(
                "Unlimited probation extension at employer’s discretion may be considered unfair."
            )

        if re.search(r"salary|wages", text) and re.search(r"deduct|withhold", text):
            issues.append(
                "Salary deductions must comply with the Payment of Wages Act."
            )

        if "gratuity" not in text and re.search(r"termination|resignation", text):
            issues.append(
                "Absence of gratuity reference may be non-compliant with the Payment of Gratuity Act."
            )

    # =================================================
    # 🔴 LEASE / RENT CONTRACTS
    # =================================================
    if "lease" in ct or "rent" in ct:

        if re.search(r"security deposit|advance", text):
            if re.search(r"any dues|owner'?s discretion|deduct any amount", text):
                issues.append(
                    "Unrestricted security deposit deductions may be legally challenged."
                )

        if re.search(r"enter the premises|take possession", text) and "notice" not in text:
            issues.append(
                "Right of entry without notice may violate tenant privacy rights."
            )

    # =================================================
    # 🔴 NON-COMPETE / RESTRAINT OF TRADE
    # =================================================
    if re.search(r"non[- ]?compete|restraint of trade", text):
        issues.append(
            "Non-compete clauses are generally unenforceable under Section 27 of the Indian Contract Act."
        )

    # =================================================
    # 🔴 INDEMNITY / LIABILITY
    # =================================================
    if re.search(r"indemnify", text) and re.search(r"all losses|any and all", text):
        issues.append(
            "Broad indemnity clauses should be limited to direct and foreseeable losses."
        )

    if re.search(r"unlimited liability|without limit|fully liable", text):
        issues.append(
            "Unlimited liability clauses may be commercially unreasonable."
        )

    # =================================================
    # 🟡 CONFIDENTIALITY / NDA
    # =================================================
    if re.search(r"confidential|nda", text):
        if re.search(r"forever|indefinite|perpetual", text):
            issues.append(
                "Indefinite confidentiality obligations may be considered unreasonable."
            )

    # =================================================
    # 🟡 IP / OWNERSHIP
    # =================================================
    if re.search(r"intellectual property|ip rights", text):
        if re.search(r"permanent|forever", text) and "compensation" not in text:
            issues.append(
                "Permanent IP transfer without compensation may be legally risky."
            )

    # =================================================
    # 🟡 ARBITRATION / JURISDICTION (ONLY IF PRESENT)
    # =================================================
    if "arbitration" in text:
        if re.search(r"sole arbitrator appointed by", text):
            issues.append(
                "Unilateral appointment of arbitrators may violate neutrality principles."
            )

        if not re.search(r"seat|venue|place", text):
            issues.append(
                "Arbitration clauses should specify seat or venue."
            )

    if re.search(r"foreign jurisdiction|outside india", text):
        issues.append(
            "Foreign jurisdiction clauses may increase enforcement difficulty."
        )

    # =================================================
    # 🟡 PRIVACY / DATA
    # =================================================
    if re.search(r"personal data|biometric|background check", text):
        if "consent" not in text:
            issues.append(
                "Collection of personal data without consent may violate privacy principles."
            )

    # =================================================
    # ✅ FINAL CLEAN OUTPUT
    # =================================================
    return sorted(set(issues))

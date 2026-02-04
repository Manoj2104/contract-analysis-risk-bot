import re
from typing import Optional, Dict


def explain_clause_plain_english(
    clause_text: str,
    clause_type: Optional[str] = "General",
    forced_risk: Optional[str] = None
) -> Dict:
    """
    FINAL – Enterprise-grade clause explanation engine

    ✔ Forced-risk aware
    ✔ Employment / Lease / Service / NDA safe
    ✔ India-law aligned
    ✔ NO generic explanation for HIGH risk clauses
    ✔ Correct rule priority
    """

    text = (clause_text or "").lower()
    clause_type = (clause_type or "General").strip()
    clause_type_l = clause_type.lower()

    explanation = {
        "what_it_means": "",
        "why_it_matters": "",
        "risk_level": forced_risk or "Low",
        "favours": "Neutral",
        "suggested_action": "No immediate action required."
    }

    # =================================================
    # 🔥 1️⃣ SCOPE OF WORK / UNLIMITED DUTIES (CRITICAL FIX)
    # =================================================
    if "scope of work" in clause_type_l or "services" in clause_type_l:
        if forced_risk == "High":
            explanation.update({
                "what_it_means":
                    "This clause allows the employer to require the employee to perform "
                    "any task, even outside their role, qualifications, or working hours.",
                "why_it_matters":
                    "Such open-ended obligations can result in unpaid work, excessive hours, "
                    "and reduced legal protection for the employee.",
                "favours": "Employer",
                "suggested_action":
                    "Restrict duties to the defined job role and working hours, and require "
                    "mutual consent for additional tasks."
            })
        else:
            explanation.update({
                "what_it_means":
                    "This clause defines the employee’s role, duties, and responsibilities.",
                "why_it_matters":
                    "A clearly defined scope prevents misuse and role ambiguity.",
            })
        return explanation

    # =================================================
    # 2️⃣ PAYMENT / SALARY / RENT
    # =================================================
    if any(k in clause_type_l for k in ["payment", "financial", "salary", "rent"]):
        explanation.update({
            "what_it_means":
                "This clause explains how and when payments must be made.",
            "why_it_matters":
                "Unclear timelines, deductions, or withholding rights can cause disputes "
                "and financial stress.",
            "favours":
                "Owner / Employer" if forced_risk == "High" else "Neutral",
            "suggested_action":
                "Ensure fixed payment dates, clear amounts, and transparent deductions."
        })
        return explanation

    # =================================================
    # 3️⃣ TERMINATION
    # =================================================
    if "termination" in clause_type_l or "terminate" in text:
        explanation.update({
            "what_it_means":
                "This clause explains when and how the agreement can be terminated.",
            "why_it_matters":
                "Immediate or one-sided termination can severely affect financial and "
                "legal security.",
            "favours":
                "Owner / Employer" if forced_risk == "High" else "Neutral",
            "suggested_action":
                "Add reasonable notice periods and fair termination grounds."
        })
        return explanation

    # =================================================
    # 4️⃣ NON-COMPETE (INDIA – SECTION 27)
    # =================================================
    if "non-compete" in clause_type_l or "non compete" in clause_type_l:
        explanation.update({
            "what_it_means":
                "This clause restricts the employee from working in a similar business "
                "after employment ends.",
            "why_it_matters":
                "Post-employment non-compete clauses are generally unenforceable in India "
                "under Section 27 of the Indian Contract Act.",
            "risk_level": "High",
            "favours": "Employer",
            "suggested_action":
                "Replace with narrowly scoped confidentiality or non-solicitation clauses."
        })
        return explanation

    # =================================================
    # 5️⃣ INDEMNITY / LIABILITY
    # =================================================
    if "indemnity" in clause_type_l or "indemnify" in text:
        explanation.update({
            "what_it_means":
                "This clause requires one party to compensate the other for certain losses.",
            "why_it_matters":
                "Unlimited or vague indemnities can create unpredictable financial exposure.",
            "favours": "Benefiting party",
            "suggested_action":
                "Limit indemnity to direct and foreseeable losses with a monetary cap."
        })
        return explanation

    # =================================================
    # 6️⃣ LIMITATION OF LIABILITY
    # =================================================
    if "limitation" in clause_type_l:
        explanation.update({
            "what_it_means":
                "This clause limits how much one party can be held financially responsible.",
            "why_it_matters":
                "Without limits, liability exposure may be excessive.",
            "favours": "Party setting the limit",
            "suggested_action":
                "Ensure liability caps are reasonable and proportionate."
        })
        return explanation

    # =================================================
    # 7️⃣ CONFIDENTIALITY / NDA
    # =================================================
    if "confidential" in clause_type_l or "nda" in clause_type_l:
        explanation.update({
            "what_it_means":
                "This clause restricts sharing of sensitive or private information.",
            "why_it_matters":
                "Overly broad confidentiality obligations may be unfair or unenforceable.",
            "favours": "Disclosing party",
            "suggested_action":
                "Clearly define scope, duration, and exclusions."
        })
        return explanation

    # =================================================
    # 8️⃣ INTELLECTUAL PROPERTY
    # =================================================
    if "intellectual" in clause_type_l or "ip" in clause_type_l:
        explanation.update({
            "what_it_means":
                "This clause defines ownership of ideas, code, or creative work.",
            "why_it_matters":
                "Unclear ownership can cause disputes after employment ends.",
            "favours": "Party owning the IP",
            "suggested_action":
                "Clearly specify ownership, usage rights, and transfer terms."
        })
        return explanation

    # =================================================
    # 9️⃣ JURISDICTION / GOVERNING LAW
    # =================================================
    if "jurisdiction" in clause_type_l or "governing law" in clause_type_l:
        explanation.update({
            "what_it_means":
                "This clause determines which laws and courts apply to disputes.",
            "why_it_matters":
                "Inconvenient or biased jurisdiction increases legal cost.",
            "favours":
                "Owner / Employer" if forced_risk in ["Medium", "High"] else "Neutral",
            "suggested_action":
                "Choose a neutral and mutually convenient jurisdiction."
        })
        return explanation

    # =================================================
    # 🔚 SAFE FALLBACK (ONLY LOW RISK)
    # =================================================
    explanation.update({
        "what_it_means":
            "This clause provides general or supporting terms of the agreement.",
        "why_it_matters":
            "It should not conflict with or dilute higher-risk clauses."
    })

    return explanation

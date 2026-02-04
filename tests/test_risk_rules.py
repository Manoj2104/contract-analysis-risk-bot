from app.modules.risk_rules import assess_risk

clause = """
The Company may terminate the employment of the Employee at any time without prior notice.
"""

result = assess_risk(clause)

print(result)

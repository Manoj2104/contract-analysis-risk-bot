def explain_risk_plain(risk_level):
    if risk_level == "High":
        return "This clause heavily favors the other party and could cause serious financial or legal trouble."
    elif risk_level == "Medium":
        return "This clause is somewhat risky and should be reviewed or clarified."
    return "This clause is generally safe and standard."

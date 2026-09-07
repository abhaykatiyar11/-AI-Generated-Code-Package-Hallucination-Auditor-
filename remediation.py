def calculate_score(findings):
    """Calculates a security score out of 100 based on findings severity."""
    if not findings:
        return 100
    
    score = 100
    for finding in findings:
        severity = getattr(finding, "severity", "Low")
        if severity == "Critical":
            score -= 25
        elif severity == "High":
            score -= 15
        elif severity == "Medium":
            score -= 10
        elif severity == "Low":
            score -= 5
            
    return max(0, score)

def calculate_security_score(findings):
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

def generate_remediation_summary(findings):
    """Generates a brief summary text of the security findings."""
    total = len(findings)
    critical = sum(1 for f in findings if getattr(f, "severity", "") == "Critical")
    high = sum(1 for f in findings if getattr(f, "severity", "") == "High")
    
    if total == 0:
        return "No vulnerabilities found. Code looks secure."
    return f"Found {total} total issues: {critical} critical and {high} high severity risks."

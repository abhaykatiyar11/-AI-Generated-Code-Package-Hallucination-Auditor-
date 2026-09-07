def generate_remediation(findings: list) -> list[dict]:
    return [
        {
            "severity": f.severity,
            "category": f.category,
            "problem": f.message,
            "fix": f.remediation
        }
        for f in findings
    ]


def calculate_score(findings: list) -> int:
    deduction = sum(f.score for f in findings)
    return max(0, 100 - deduction)
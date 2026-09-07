from dataclasses import dataclass
from typing import Optional


@dataclass
class Finding:
    def __init__(self, severity: str, category: str, message: str, remediation: str = "", line: int = None, code: str = None):
        self.severity = severity          # "Critical", "High", "Medium", "Low"
        self.category = category          # e.g., "Package Hallucination", "Hardcoded Secret"
        self.message = message            # Detailed explanation
        self.remediation = remediation    # Fix suggestion
        self.line = line                  # Line number in code
        self.code = code                  # Snippet causing issue

    @property
    def score(self) -> int:
        return {
            "Critical": 25,
            "High": 15,
            "Medium": 8,
            "Low": 3,
            "Info": 0
        }.get(self.severity, 0)

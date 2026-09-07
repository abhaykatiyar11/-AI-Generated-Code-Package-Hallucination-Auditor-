from dataclasses import dataclass
from typing import Optional


@dataclass
class Finding:
    severity: str
    category: str
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    code: Optional[str] = None
    remediation: Optional[str] = None

    @property
    def score(self) -> int:
        return {
            "Critical": 25,
            "High": 15,
            "Medium": 8,
            "Low": 3,
            "Info": 0
        }.get(self.severity, 0)
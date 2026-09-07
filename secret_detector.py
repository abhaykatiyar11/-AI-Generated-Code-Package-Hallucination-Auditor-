import re

SECRET_PATTERNS = [
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Generic API Key", re.compile(r"(?i)\b(api[_-]?key|apikey)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
    ("Password", re.compile(r"(?i)\b(password|passwd|pwd)\b\s*[:=]\s*['\"][^'\"]+['\"]")),
    ("Secret Token", re.compile(r"(?i)\b(secret|token|auth[_-]?token)\b\s*[:=]\s*['\"][^'\"]+['\"]")),
]


def detect_secrets(source: str):import re

SECRET_PATTERNS = [
    ("AWS Access Key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Generic API Key", re.compile(r"(?i)\b(api[_-]?key|apikey)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]")),
    ("Password", re.compile(r"(?i)\b(password|passwd|pwd)\b\s*[:=]\s*['\"][^'\"]+['\"]")),
    ("Secret Token", re.compile(r"(?i)\b(secret|token|auth[_-]?token)\b\s*[:=]\s*['\"][^'\"]+['\"]")),
]


def detect_secrets(source: str):
    findings = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append({
                    "name": name,
                    "line": line_number,
                    "text": line.strip()
                })
    return findings
    findings = []
    for line_number, line in enumerate(source.splitlines(), start=1):
        for name, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append({
                    "name": name,
                    "line": line_number,
                    "text": line.strip()
                })
    return findings

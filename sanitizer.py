import re

def suggest_sanitized_code(code: str) -> str:
    """Basic sanitizer that masks hardcoded secrets and replaces risky functions."""
    # Mask potential API keys or secret strings
    sanitized = re.sub(r'(['"'])(sk-[a-zA-Z0-9_-]{20,})\1', r'\1REDACTED_API_KEY\1', code)
    
    # Replace dangerous eval or pickle usage suggestions
    sanitized = sanitized.replace("eval(", "# TODO: Avoid eval()\n# eval(")
    
    return sanitized

import re

def sanitize_secrets(code: str):
    """Scans code for hardcoded secrets, replaces them, and generates an env template."""
    env_lines = []
    sanitized_code = code

    # Pattern to find simple hardcoded API keys or secrets in quotes
    secret_pattern = re.compile(r'(['"\'])(sk-[a-zA-Z0-9_-]{15,}|secret_[a-zA-Z0-9_-]{15,})\1')
    matches = secret_pattern.findall(code)

    for quote, secret in matches:
        env_lines.append(f"SECRET_KEY={secret}")
        sanitized_code = sanitized_code.replace(secret, 'os.getenv("SECRET_KEY")')

    env_example = "\n".join(env_lines) if env_lines else ""
    return sanitized_code, env_example

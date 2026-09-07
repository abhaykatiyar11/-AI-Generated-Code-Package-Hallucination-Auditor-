import re


def sanitize_secrets(source: str):
    env_variables = []
    lines = source.splitlines()
    sanitized = []

    pattern = re.compile(
        r"(?P<key>api[_-]?key|apikey|password|passwd|pwd|secret|token|auth[_-]?token)"
        r"(\s*=\s*)"
        r"(?P<quote>['\"])(?P<value>[^'\"]+)(?P=quote)",
        re.IGNORECASE
    )

    for line in lines:
        match = pattern.search(line)
        if match:
            key = match.group("key").upper()
            env_name = re.sub(r"[^A-Z0-9]+", "_", key)
            env_variables.append(env_name)

            replacement = f"os.getenv('{env_name}')"
            line = line[:match.start()] + match.group("key") + " = " + replacement + line[match.end():]

        sanitized.append(line)

    sanitized_source = "\n".join(sanitized)
    if env_variables and "import os" not in sanitized_source:
        sanitized_source = "import os\n\n" + sanitized_source

    env_example = "\n".join(f"{name}=" for name in sorted(set(env_variables)))
    return sanitized_source, env_example
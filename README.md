# 🛡️ CodeSanitizer

AI-Generated Code & Package Hallucination Auditor.

CodeSanitizer detects security problems commonly introduced by AI-generated Python code.

## Features

- AST-based Python security analysis
- Hardcoded secret detection
- Dangerous function detection
- Unsafe deserialization detection
- Command injection detection
- PyPI package verification
- Async dependency checking
- Security score
- Remediation recommendations
- .env.example generation
- Sanitized code download
- Streamlit dashboard
- CLI/pre-commit ready architecture

## Run locally

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run:

streamlit run app.py

## Security Architecture

CodeSanitizer parses Python source code using Python's AST module.

Imports are extracted from the syntax tree and verified against PyPI.

Security findings are assigned severity levels and remediation guidance.

## Important

Package existence on PyPI does not prove that a package is safe.

CodeSanitizer is an auditing aid and should be combined with dependency pinning, trusted package sources, code review, and other security controls.

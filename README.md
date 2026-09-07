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
{
  "project": "CodeSanitizer",
  "title": "AI-Generated Code & Package Hallucination Auditor",
  "flowchart": {
    "start": {
      "id": "START",
      "type": "start",
      "label": "Start CodeSanitizer"
    },

    "input": {
      "id": "INPUT",
      "type": "process",
      "label": "Input Python Code",
      "description": "User pastes or uploads Python source code through Streamlit or CLI"
    },

    "parse": {
      "id": "AST_PARSE",
      "type": "process",
      "label": "Parse Code Using Python AST",
      "description": "Use ast.parse() to convert source code into an Abstract Syntax Tree"
    },

    "syntax_check": {
      "id": "SYNTAX_CHECK",
      "type": "decision",
      "label": "Valid Python Syntax?"
    },

    "syntax_error": {
      "id": "SYNTAX_ERROR",
      "type": "output",
      "label": "Display Syntax Error",
      "description": "Show line and error information and stop scanning"
    },

    "ast_analysis": {
      "id": "AST_ANALYSIS",
      "type": "process",
      "label": "Traverse AST",
      "description": "Use ast.NodeVisitor to inspect imports, function calls, assignments, constants, attributes and other code structures"
    },

    "security_checks": {
      "id": "SECURITY_CHECKS",
      "type": "parallel",
      "label": "Parallel Security Analysis",
      "branches": [
        {
          "id": "DANGEROUS_FUNCTIONS",
          "label": "Dangerous Function Detection",
          "checks": [
            "eval()",
            "exec()",
            "compile()",
            "__import__()",
            "subprocess with shell=True"
          ]
        },
        {
          "id": "SECRET_DETECTION",
          "label": "Hardcoded Secret Detection",
          "checks": [
            "API keys",
            "Passwords",
            "Tokens",
            "Authentication credentials",
            "Cloud credentials"
          ]
        },
        {
          "id": "DESERIALIZATION",
          "label": "Unsafe Deserialization Detection",
          "checks": [
            "pickle.loads()",
            "yaml.load()",
            "Other unsafe deserialization patterns"
          ]
        },
        {
          "id": "IMPORT_EXTRACTION",
          "label": "Dependency Extraction",
          "checks": [
            "import statements",
            "from ... import statements",
            "External package names",
            "Ignore Python standard library modules"
          ]
        }
      ]
    },

    "dependency_verification": {
      "id": "PYPI_CHECK",
      "type": "async_process",
      "label": "Asynchronous PyPI Verification",
      "description": "Check external packages concurrently using the PyPI JSON API",
      "steps": [
        "Normalize import names",
        "Remove standard-library packages",
        "Create asynchronous HTTP requests",
        "Check whether package exists",
        "Retrieve package version and metadata",
        "Handle timeout and network errors",
        "Detect potentially hallucinated packages"
      ]
    },

    "aggregate": {
      "id": "AGGREGATE",
      "type": "process",
      "label": "Aggregate Security Findings",
      "description": "Combine AST findings, secret findings and package verification results"
    },

    "severity": {
      "id": "SEVERITY",
      "type": "process",
      "label": "Assign Severity",
      "levels": {
        "Critical": [
          "Arbitrary code execution",
          "Unsafe pickle deserialization",
          "Highly dangerous dependency"
        ],
        "High": [
          "Hardcoded credentials",
          "eval()",
          "exec()",
          "shell=True",
          "Non-existent package"
        ],
        "Medium": [
          "Unsafe compile()",
          "yaml.load()",
          "Suspicious dynamic import"
        ],
        "Low": [
          "Weak security patterns",
          "Potentially suspicious behavior"
        ],
        "Info": [
          "Package metadata",
          "Version information",
          "Informational warnings"
        ]
      }
    },

    "score": {
      "id": "SECURITY_SCORE",
      "type": "process",
      "label": "Calculate Security Score",
      "description": "Calculate a score from 0-100 based on detected vulnerabilities and severity"
    },

    "remediation": {
      "id": "REMEDIATION",
      "type": "process",
      "label": "Generate Remediation Recommendations",
      "description": "Provide practical fixes for every security finding",
      "examples": [
        "Replace eval() with safe parsing",
        "Replace pickle with JSON for untrusted data",
        "Use subprocess argument lists instead of shell=True",
        "Move secrets to environment variables",
        "Verify package names before installation",
        "Replace unsafe YAML loading with yaml.safe_load()"
      ]
    },

    "secret_check": {
      "id": "SECRET_FOUND",
      "type": "decision",
      "label": "Hardcoded Secret Found?"
    },

    "sanitization": {
      "id": "SANITIZATION",
      "type": "bonus_process",
      "label": "Generate Sanitized Code",
      "description": "Replace hardcoded secrets with environment-variable references",
      "outputs": [
        "sanitized.py",
        ".env.example"
      ]
    },

    "dashboard": {
      "id": "DASHBOARD",
      "type": "output",
      "label": "Display Streamlit Security Dashboard",
      "components": [
        "Security score",
        "Critical findings",
        "High findings",
        "Medium findings",
        "Low findings",
        "Package verification results",
        "Detected secrets",
        "AST security findings",
        "Remediation recommendations",
        "Sanitized code download",
        ".env.example download"
      ]
    },

    "decision": {
      "id": "SECURITY_DECISION",
      "type": "decision",
      "label": "Security Threshold Passed?"
    },

    "pass": {
      "id": "PASS",
      "type": "output",
      "label": "PASS",
      "description": "Code passed the configured security threshold"
    },

    "block": {
      "id": "BLOCK",
      "type": "output",
      "label": "BLOCK",
      "description": "Code contains security issues that exceed the configured threshold"
    },

    "precommit": {
      "id": "PRE_COMMIT",
      "type": "process",
      "label": "Pre-Commit Security Gate",
      "description": "Optionally execute CodeSanitizer before code is committed"
    },

    "github": {
      "id": "GITHUB",
      "type": "deployment",
      "label": "Push Project to GitHub",
      "steps": [
        "git add .",
        "git commit",
        "git push"
      ]
    },

    "streamlit": {
      "id": "STREAMLIT",
      "type": "deployment",
      "label": "Deploy Through Streamlit Community Cloud",
      "steps": [
        "Connect GitHub repository",
        "Select main branch",
        "Select app.py",
        "Deploy application"
      ]
    },

    "live_app": {
      "id": "LIVE_APP",
      "type": "end",
      "label": "Live CodeSanitizer Application"
    }
  },

  "connections": [
    ["START", "INPUT"],
    ["INPUT", "AST_PARSE"],
    ["AST_PARSE", "SYNTAX_CHECK"],

    ["SYNTAX_CHECK:No", "SYNTAX_ERROR"],
    ["SYNTAX_CHECK:Yes", "AST_ANALYSIS"],

    ["AST_ANALYSIS", "SECURITY_CHECKS"],

    ["SECURITY_CHECKS:IMPORT_EXTRACTION", "PYPI_CHECK"],
    ["SECURITY_CHECKS:DANGEROUS_FUNCTIONS", "AGGREGATE"],
    ["SECURITY_CHECKS:SECRET_DETECTION", "AGGREGATE"],
    ["SECURITY_CHECKS:DESERIALIZATION", "AGGREGATE"],
    ["PYPI_CHECK", "AGGREGATE"],

    ["AGGREGATE", "SEVERITY"],
    ["SEVERITY", "SECURITY_SCORE"],
    ["SECURITY_SCORE", "REMEDIATION"],

    ["REMEDIATION", "SECRET_FOUND"],
    ["SECRET_FOUND:Yes", "SANITIZATION"],
    ["SECRET_FOUND:No", "DASHBOARD"],
    ["SANITIZATION", "DASHBOARD"],

    ["DASHBOARD", "SECURITY_DECISION"],
    ["SECURITY_DECISION:Yes", "PASS"],
    ["SECURITY_DECISION:No", "BLOCK"],

    ["PASS", "PRE_COMMIT"],
    ["BLOCK", "PRE_COMMIT"],

    ["PRE_COMMIT", "GITHUB"],
    ["GITHUB", "STREAMLIT"],
    ["STREAMLIT", "LIVE_APP"]
  ],

  "overall_flow": [
    "START",
    "INPUT",
    "AST_PARSE",
    "SYNTAX_CHECK",
    "AST_ANALYSIS",
    "PARALLEL_SECURITY_CHECKS",
    "ASYNC_PYPI_VERIFICATION",
    "AGGREGATE_FINDINGS",
    "SEVERITY_CLASSIFICATION",
    "SECURITY_SCORE",
    "REMEDIATION",
    "SECRET_DETECTION_DECISION",
    "SANITIZED_CODE_AND_ENV_EXAMPLE",
    "STREAMLIT_DASHBOARD",
    "SECURITY_THRESHOLD",
    "PASS_OR_BLOCK",
    "PRE_COMMIT_GATE",
    "GITHUB",
    "STREAMLIT_CLOUD",
    "LIVE_APP"
  ]
}
